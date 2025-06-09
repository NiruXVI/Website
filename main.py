import flet as ft

def main(page: ft.Page):
    MOBILE_WIDTH = 375
    MOBILE_HEIGHT = 700

    page.title = "Fletstagram"
    page.window_width = MOBILE_WIDTH
    page.window_height = MOBILE_HEIGHT
    page.bgcolor = "#fafafa"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    posts = []

    FEED_HEIGHT = MOBILE_HEIGHT - 190

    feed = ft.ListView(
        expand=False,
        height=FEED_HEIGHT,
        spacing=12,
        padding=ft.padding.symmetric(horizontal=0, vertical=8),
        auto_scroll=True,
    )

    post_field = ft.TextField(
        label="Share something…",
        multiline=True,
        min_lines=1,
        max_lines=3,
        expand=True,
        border_radius=12,
        height=48,
        dense=True,
        bgcolor="#f0f2f5",
    )
    image_picker = ft.FilePicker()
    picked_image = {"src": None}

    input_image_preview = ft.Container(
        width=MOBILE_WIDTH-48,
        height=100,
        alignment=ft.alignment.center,
        border_radius=10,
        margin=ft.margin.only(bottom=8),
        visible=False,
        bgcolor="#e4e4e4",
        content=None,
    )

    def pick_image(e):
        image_picker.pick_files(allow_multiple=False, file_type="image")

    def on_image_picked(e: ft.FilePickerResultEvent):
        if e.files:
            picked_image["src"] = e.files[0].path
            input_image_preview.content = ft.Image(
                src=picked_image["src"],
                width=MOBILE_WIDTH-60,
                height=90,
                fit=ft.ImageFit.CONTAIN,
                border_radius=8,
            )
            input_image_preview.visible = True
            page.snack_bar = ft.SnackBar(ft.Text("Image selected!"))
            page.snack_bar.open = True
        else:
            picked_image["src"] = None
            input_image_preview.content = None
            input_image_preview.visible = False
        page.update()

    def remove_image_preview(e):
        picked_image["src"] = None
        input_image_preview.content = None
        input_image_preview.visible = False
        page.update()

    def add_post(e):
        text = post_field.value.strip()
        img = picked_image["src"]
        if text or img:
            post = {
                "user": "user" + str(len(posts) % 3 + 1),
                "text": text,
                "img": img,
                "likes": 0,
                "comments": [],
            }
            posts.insert(0, post)
            post_field.value = ""
            picked_image["src"] = None
            input_image_preview.content = None
            input_image_preview.visible = False
            refresh_feed()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Please enter text or pick an image."))
            page.snack_bar.open = True
        page.update()

    def like_post(index):
        posts[index]["likes"] += 1
        refresh_feed()

    def add_comment(index, comment_field):
        comment = comment_field.value.strip()
        if comment:
            posts[index]["comments"].append(comment)
            comment_field.value = ""
            refresh_feed()
        page.update()

    def refresh_feed():
        feed.controls.clear()
        for idx, post in enumerate(posts):
            post_widgets = [
                ft.Row([
                    ft.CircleAvatar(content=ft.Text(post["user"][0].upper()), radius=18, bgcolor="#3897f0"),
                    ft.Text(f"@{post['user']}", weight="bold", size=14),
                ], spacing=8),
            ]
            if post["img"]:
                post_widgets.append(
                    ft.Container(
                        ft.Image(src=post["img"], width=MOBILE_WIDTH - 36, height=200, fit=ft.ImageFit.COVER),
                        border_radius=12,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    )
                )
            if post["text"]:
                post_widgets.append(ft.Text(post["text"], size=15))
            post_widgets.append(
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.FAVORITE_BORDER,
                        icon_color="#ed4956",
                        tooltip="Like",
                        on_click=lambda e, i=idx: like_post(i),
                    ),
                    ft.Text(str(post["likes"])),
                ], spacing=4)
            )
            comment_field = ft.TextField(
                hint_text="Add a comment…", width=160, dense=True, height=30, border_radius=8, bgcolor="#f0f2f5"
            )
            post_widgets.append(
                ft.Column([
                    ft.Row([
                        comment_field,
                        ft.IconButton(
                            icon=ft.Icons.SEND,
                            tooltip="Comment",
                            on_click=lambda e, i=idx, f=comment_field: add_comment(i, f),
                            icon_color="#3897f0"
                        ),
                    ], spacing=4),
                    ft.Column([ft.Text(f"- {c}", italic=True, size=12) for c in post["comments"]], spacing=2),
                ])
            )
            feed.controls.append(
                ft.Card(
                    ft.Container(
                        ft.Column(post_widgets, spacing=7),
                        padding=12,
                        width=MOBILE_WIDTH - 28,
                        bgcolor="white",
                        border_radius=14,
                    ),
                    elevation=4,
                    margin=ft.margin.symmetric(horizontal=2, vertical=5),
                )
            )
        page.update()

    image_btn = ft.IconButton(
        icon=ft.Icons.IMAGE,
        tooltip="Pick Image",
        on_click=pick_image,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        icon_color="#3897f0",
        bgcolor="#f0f2f5",
    )

    remove_img_btn = ft.IconButton(
        icon=ft.Icons.CLOSE,
        tooltip="Remove Image",
        on_click=remove_image_preview,
        icon_color="red",
        bgcolor="#f8eaea",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        visible=True,
    )

    post_btn = ft.IconButton(
        icon=ft.Icons.SEND,
        tooltip="Post",
        on_click=add_post,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        icon_color="#3897f0",
        bgcolor="#f0f2f5",
    )

    page.overlay.append(image_picker)
    image_picker.on_result = on_image_picked

    # Notice: No expand=True in the Column, and Container has explicit height
    page.add(
        ft.Container(
            ft.Column(
                [
                    ft.Container(
                        ft.Text("Fletstagram", size=22, weight="bold", color="#262626", text_align=ft.TextAlign.CENTER),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=12, bottom=4),
                        width=MOBILE_WIDTH,
                    ),
                    ft.Row(
                        [
                            input_image_preview,
                            remove_img_btn
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        visible=True,
                        spacing=4,
                    ),
                    ft.Container(
                        ft.Row(
                            [post_field, image_btn, post_btn],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        padding=ft.padding.symmetric(horizontal=6, vertical=6),
                        width=MOBILE_WIDTH,
                    ),
                    ft.Divider(height=1, color="#e0e0e0"),
                    ft.Text("Feed", size=16, weight="bold", color="#888"),
                    ft.Container(
                        feed,
                        width=MOBILE_WIDTH,
                        height=FEED_HEIGHT,
                        alignment=ft.alignment.top_center,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=MOBILE_WIDTH,
            height=MOBILE_HEIGHT,
            bgcolor="#fafafa",
            border_radius=22,
            alignment=ft.alignment.top_center,
            margin=0,
            padding=0,
            border=ft.border.all(2, "#3897f0"),
        )
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)