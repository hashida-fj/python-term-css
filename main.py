from termcss import TermCss
from zenlog import log

log.level("error")

tobi = {
    'name': "tobi",
    'species': "ferret",
    'age': 2,
    'loglevel': "DEBUG"
}

tcss = TermCss.fromFile("pet.css")

template = "{name} is a {species}, he is {age} years old"
fn = tcss.compile(template)

mark = "{loglevel}\n"
template = "{name} は {species}で {age}歳だよ！"

fn2 = tcss.compile([mark, template])


print(fn(tobi))
print(fn2(tobi))


