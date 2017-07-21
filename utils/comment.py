


def comment_tree(comment_list):
    # [{'child': [{'child': [{'child': [], 'user__nickname': 'egon', 'content': '哪里不好啊', 'create_time': None, 'id': 3, 'parent_id': 2}],
    #              'user__nickname': 'sever', 'content': '扯淡', 'create_time': None, 'id': 2, 'parent_id': 1}],
    #   'user__nickname': 'egon', 'content': '写的太好了', 'create_time': None, 'id': 1, 'parent_id': None},
    #  {'child': [], 'user__nickname': 'root', 'content': '写的不错', 'create_time': None, 'id': 4, 'parent_id': None},
    #  {'child': [], 'user__nickname': 'alex', 'content': '我写的真好', 'create_time': None, 'id': 5, 'parent_id': None}]

    comment_str="<div class='comment'>"
    for row in comment_list:
        tpl="<div class='content'>%s:%s --- %s</div>"%(row['user__nickname'],row['content'],row['create_time'])
        comment_str += tpl
        if row['child']:

            child_str=comment_tree(row['child'])
            comment_str += child_str
    comment_str += '</div>'
    return comment_str



