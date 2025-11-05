import asyncio
import os
import zipfile
import tempfile
import random
import subprocess
import json
import glob
import shutil

from playwright.async_api import async_playwright, Playwright, Page

from dotenv import load_dotenv

load_dotenv()


def reduce(toReduce: str):
    toReduce = toReduce.strip()
    toReduce = toReduce.replace(":", "")

    if len(toReduce) > 64:
        return f"{toReduce[:31]}___{toReduce[len(toReduce) - 30:]}"

    return toReduce


async def extract_course_list(page: Page):
    """
    From chatgpt, modified
    """
    await page.goto("https://www.moodle.tum.de/my", timeout=0)

    courses = []  # type: ignore

    course_links = page.locator("#coc-courselist h3 a")

    count = await course_links.count()
    for i in range(count):
        name = await (
            course_links.nth(i).get_attribute("title")
            or course_links.nth(i).inner_text().split("\n")[0].strip()
        )
        url = await course_links.nth(i).get_attribute("href")

        if name:
            name = name.strip()

        if name and url:
            courses.append({"name": name, "url": url})

    return courses


async def download_course_attachments(page: Page, courseUrl: str, courseName: str):
    print(f"Downloading: {courseName}")

    await page.goto(courseUrl, timeout=0)
    await page.click(".nav-link.downloadcenterlink")
    await page.wait_for_timeout(5000)

    # Extract all downloadable files
    possible_dirs = await (await page.query_selector(".mform")).query_selector_all(
        ".card.block.mb-3"
    )

    files = []
    for dir in possible_dirs:
        dir_files = await dir.query_selector_all("label")
        skip_first = True

        for file in dir_files:
            if skip_first:
                skip_first = False
                continue

            file_info = {
                "folder": await (
                    await dir.query_selector(".sectiontitle.mt-1")
                ).inner_text(),
                "filename": (
                    reduce(
                        await (
                            await file.query_selector(".itemtitle > span")
                        ).inner_text()
                    )
                )
                .replace(":", "")
                .replace("/", "")
                .split(".")[0],
                "selectId": (await file.get_attribute("for")),
                "pdf": await (
                    await file.query_selector(".itemtitle > img")
                ).get_attribute("alt")
                == "Datei",
            }
            files.append(file_info)

    # Filter out already downloaded files
    ids_to_select_and_download = []

    for file in files:
        # Check if it exists locally
        globbed = glob.glob(
            f"{os.getenv("DATA_DIR")}/{courseName}/{file['folder']}/{file['filename']}*"
        )

        if len(globbed) == 1:
            # Found, skipping
            continue
        if len(globbed) > 1:
            # Multiple files start with the same name, try to get a exact match up to file ending
            if (
                len(
                    [
                        i
                        for i, item in enumerate(globbed)
                        if item.startswith(
                            f"{os.getenv("DATA_DIR")}/{courseName}/{file['folder']}/{file['filename']}."
                        )
                    ]
                )
                == 1
            ):

                continue

        # Else add to download list
        print(f"Found new file: {file['folder']}/{file['filename']}")
        ids_to_select_and_download.append(file["selectId"])

    if len(ids_to_select_and_download) == 0:
        print(f"Nothing new for course: {courseName}")
        return

    # Deselect everything
    await page.click("#downloadcenter-none-included")

    # And gradually select what to download
    for id in ids_to_select_and_download:
        await page.click(f"#{id}")

    # ===

    # Handle download event
    async with page.expect_download() as download_info:
        await page.click("#id_submitbutton")

    download = await download_info.value

    # Prepare tmp extraction dir
    TEMP_DIR = tempfile.gettempdir()
    ZIP_LOCAL_PATH = f"{TEMP_DIR}/moodle-{random.randint(0, 999999)}/"

    os.makedirs(ZIP_LOCAL_PATH, exist_ok=True)
    os.makedirs(ZIP_LOCAL_PATH + "extracted", exist_ok=True)

    print(f"Downloading to: {ZIP_LOCAL_PATH + download.suggested_filename}")

    await download.save_as(ZIP_LOCAL_PATH + download.suggested_filename)

    print(f"Unzipping to: {ZIP_LOCAL_PATH}extracted")

    # Unzip file
    COPY_TARGET_PATH = f"{os.getenv('DATA_DIR')}/{courseName}/"

    with zipfile.ZipFile(ZIP_LOCAL_PATH + download.suggested_filename, "r") as zip_ref:
        zip_ref.extractall(ZIP_LOCAL_PATH + "extracted")

    # Copy extracted dir in tmp to storage
    print(f"Copying to: {COPY_TARGET_PATH}")
    os.makedirs(COPY_TARGET_PATH, exist_ok=True)

    rsync_args = [
        "rsync",
        "-av",
        "--ignore-existing",
        "--backup",
        "--suffix=_modified",
        f"{ZIP_LOCAL_PATH}extracted/",
        f"{COPY_TARGET_PATH}",
    ]

    try:
        subprocess.run(args=rsync_args, stdout=subprocess.DEVNULL)
    except Exception as err:
        print("Error while coping extracted files")
        print(rsync_args)
        print(err)

    # Delete tmp downloaded & tmp extracted files
    shutil.rmtree(ZIP_LOCAL_PATH)


async def download_all_courses(page: Page):

    # Check if we should only download a specific course list
    checkCourses = False
    coursesToDownload: list[str] = []

    if os.getenv("COURSES") != None:
        print("Downloading specific courses")

        checkCourses = True
        coursesToDownload = json.loads(os.getenv("COURSES"))
    else:
        print("Downloading all courses")

    for course in await extract_course_list(page):
        if checkCourses:
            try:
                coursesToDownload.index(course["name"])
            except ValueError:
                print(f"Skipping: {course['name']}")
                continue

        await download_course_attachments(
            page, courseName=course["name"], courseUrl=course["url"]
        )

    print("Finished downloading all courses")


async def login(page: Page):
    print("Logging in")

    await page.goto("https://www.moodle.tum.de/", timeout=0)

    await page.click(".btn.btn-primary")
    await page.wait_for_url("https://login.tum.de/idp/**", timeout=0)

    await page.type("#username", os.getenv("USERNAME"))
    await page.type("#password", os.getenv("PASSWORD"))

    await page.click("#btnLogin")
    await page.wait_for_url("https://www.moodle.tum.de/**", timeout=0)

    print("Logged in")


async def run(playwright: Playwright):
    headless = True
    if os.getenv("DISABLE_HEADLESS") != None:
        headless = False

    chromium = playwright.chromium
    browser = await chromium.launch(headless=headless)
    page = await browser.new_page()

    await login(page)
    await download_all_courses(page)

    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
