from urllib.parse import quote


def search_book(book_name):
    keyword = quote(book_name)

    url = f"https://z-lib.gs/s/{keyword}"

    return (
        f"📚 Luna 图书馆\n\n"
        f"书名：{book_name}\n\n"
        f"🔎 搜索结果：\n"
        f"{url}"
    )
