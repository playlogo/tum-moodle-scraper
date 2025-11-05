def reduce(toReduce: str):
    toReduce = toReduce.strip()
    toReduce = toReduce.replace(":", "")

    if len(toReduce) > 64:
        return f"{toReduce[:31]}___{toReduce[len(toReduce) - 30:]}"

    return toReduce


print(
    reduce(
        "Ankündigung der Fachschaft Aufruf für Kandidaturen zum Semestersprecher oder Semestersprecherin"
    )
)

print(reduce("In der Klausur bereitgestellte Referenzmaterialien (falls benötigt)"))

print(
    reduce(
        "Ankündigung der Fachschaft: Aufruf für Kandidaturen zum Semestersprecher oder Semestersprecherin"
    )
)
