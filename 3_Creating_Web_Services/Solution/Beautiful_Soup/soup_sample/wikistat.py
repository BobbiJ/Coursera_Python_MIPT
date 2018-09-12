from bs4 import BeautifulSoup
import re
import os


def searcher(start, end, path, files, max_deep, now_deep, arr_searched):
    now_deep += 1
    if now_deep <= max_deep:
        if start in arr_searched:
            return None
        else:

            arr_searched.append(start)
            with open(os.path.join(path, start), 'rb') as f:
                html = f.read()
                soap = BeautifulSoup(html, 'lxml')
                tags = soap.find_all('a', href=True)
                tags_true = [tag['href'].split('/wiki/')[1] for tag in tags if '/wiki/' in tag['href']]
                if end in tags_true:
                    return [end]

                for tag in tags_true:
                    if tag in files:
                        solution = searcher(tag, end, path, files, max_deep, now_deep, arr_searched)
                        if solution is not None:
                            solution.append(tag)
                            return solution

    return None


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, end, path):
    # link_re = re.compile(r"(?<=/wiki/)[\w()]+")  # Искать ссылки можно как угодно, не обязательно через re
    files = dict.fromkeys(os.listdir(path))  # Словарь вида {"filename1": None, "filename2": None, ...}
    solution = None
    for i in range(1, 20):
        solution = searcher(start, end, path, files, i, 0, [])
        if solution is not None:
            return solution
    # TODO Проставить всем ключам в files правильного родителя в значение, начиная от start
    return solution or 0


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(start, end, path):
    final_arr = build_tree(start, end, path)
    final_arr.append(start)
    return final_arr


def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно добраться от start до end, то,
    по крайней мере, известны сами start и end, и можно распарсить хотя бы их: bridge = [end, start]. Оценка за тест,
    в этом случае, будет сильно снижена, но на минимальный проходной балл наберется, и тест будет пройден.
    Чтобы получить максимальный балл, придется искать все страницы. Удачи!
    """

    bridge = build_bridge(start, end, path)  # Искать список страниц можно как угодно, даже так: bridge = [end, start]

    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        with open(os.path.join(path, file), 'rb') as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")
        imgs = 0
        for img in body.find_all('img', width=True):
            if int(img['width']) >= 200:
                imgs += 1

        headers = 0
        for a in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            for head in body.find_all(a):
                if re.match(r'^[E,T,C]', head.text) is not None:
                    headers += 1

        linkslen = 0
        for a in body.find_all('a'):
            a_siblings = a.find_next_siblings()
            len_arr = 1
            for sib in a_siblings:
                    if sib.name == 'a':
                        len_arr+=1
                    else:
                        break
            if len_arr > linkslen:
                linkslen = len_arr

        lists = 0
        for ul in body.find_all('ul'):
            if ul.parent.name == 'div':
                lists += 1
        for ol in body.find_all('ol'):
            if ol.parent.name == 'div':
                lists += 1





        # TODO посчитать реальные значения
        # imgs = 5  # Количество картинок (img) с шириной (width) не меньше 200
        # headers = 10  # Количество заголовков, первая буква текста внутри которого: E, T или C
        # linkslen = 15  # Длина максимальной последовательности ссылок, между которыми нет других тегов
        # lists = 20  # Количество списков, не вложенных в другие списки

        out[file] = [imgs, headers, linkslen, lists]

    return out


if __name__ == '__main__':
    print(parse('Stone_Age', 'Brain', './wiki/'))
