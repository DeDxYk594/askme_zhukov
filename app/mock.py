USERS = {
    1: {"name": "Marine geologist", "avatar": "1.jpg"},
    2: {"name": "mr_beast", "avatar": "2.jpg"},
    3: {"name": "Volosatova T. M.", "avatar": "3.jpg"},
    4: {"name": "Vladimir123", "avatar": "president.jpg"},
    5: {"name": "Filolog", "avatar": "5.jpg"},
    6: {"name": "Math Expert 3.14", "avatar": "6.jpg"},
    7: {"name": "Vasily Pupkin", "avatar": "7.jpg"},
    8: {"name": "Миша Забивной", "avatar": "8.jpg"},
    9: {"name": "Director BV", "avatar": "9.jpg"},
    10: {"name": "sdsdfdsf", "avatar": "10.jpg"},
    11: {"name": "ФЫВФЫВ", "avatar": "11.jpg"},
}


QUESTIONS = [
    {
        "id": 1,
        "title": "Who is in this picture?",
        "text": 'I though very long\nLorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum для распечатки образцов. Lorem Ipsum не только успешно пережил без заметных изменений пять веков, но и перешагнул в электронный дизайн. Его популяризации в новое время послужили публикация листов Letraset с образцами Lorem Ipsum в 60-х годах и, в более недавнее время, программы электронной вёрстки типа Aldus PageMaker, в шаблонах которых используется Lorem Ipsum.',
        "image": "president.jpg",
        "rating": 5,
        "tags":["sapr"],
        "answers": [
            {
                "text": "Maybe, its president",
                "rating": 2,
                "user_id": 3,
            }
        ],
    },
    {
        "id": 2,
        "title": "What is the capital of France?",
        "text": "Test your geography knowledge",
        "tags":["sapr"],
        "image": "skala.jpg",
        "rating": 4,
        "answers": [
            {
                "text": "The capital of France is Paris",
                "rating": 5,
                "user_id": 4,
            }
        ],
    },
    {
        "id": 3,
        "title": "Who wrote the famous play 'Romeo and Juliet'?",
        "text": "A classic literary question",
        "image": "stress.jpg",
        "tags":["sapr"],
        "rating": 4,
        "answers": [
            {
                "text": "William Shakespeare wrote 'Romeo and Juliet'",
                "rating": 5,
                "user_id": 3,
            },
            {
                "text": "It was penned by an anonymous playwright",
                "rating": 4,
                "user_id": 4,
            },
        ],
    },
    {
        "id": 4,
        "title": "Who is in this picture?",
        "text": "I though very long",
        "image": "president.jpg",
        "tags":["books"],
        "rating": 5,
        "answers": [
            {
                "text": "Maybe, its president",
                "rating": 2,
                "user_id": 1,
            }
        ],
    },
    {
        "id": 5,
        "title": "What is the capital of France?",
        "text": "Test your geography knowledge",
        "image": "president.jpg",
        "tags":["books"],
        "rating": 4,
        "answers": [
            {
                "text": "The capital of France is Paris",
                "rating": 5,
                "user_id": 3,
            }
        ],
    },
    {
        "id": 6,
        "title": "Who wrote the famous play 'Romeo and Juliet'?",
        "text": "A classic literary question",
        "image": "president.jpg",
        "tags":[],
        "rating": 4,
        "answers": [
            {
                "text": "William Shakespeare wrote 'Romeo and Juliet'",
                "rating": 5,
                "user_id": 2,
            },
            {
                "text": "It was penned by an anonymous playwright",
                "rating": 4,
                "user_id": 5,
            },
        ],
    },
    {
        "id": 7,
        "title": "What is the largest mammal on Earth?",
        "text": 'Test your zoological knowledge Lorem Ipsum - это текст-"рыба", часто используемый в печати и вэб-дизайне. Lorem Ipsum является стандартной "рыбой" для текстов на латинице с начала XVI века. В то время некий безымянный печатник создал большую коллекцию размеров и форм шрифтов, используя Lorem Ipsum для распечатки образцов. Lorem Ipsum не только успешно пережил без заметных изменений пять веков, но и перешагнул в электронный дизайн. Его популяризации в новое время послужили публикация листов Letraset с образцами Lorem Ipsum в 60-х годах и, в более недавнее время, программы электронной вёрстки типа Aldus PageMaker, в шаблонах которых используется Lorem Ipsum.',
        "image": "whale.jpg",
        "tags":[],
        "rating": 4,
        "answers": [
            {
                "text": "The largest mammal is the blue whale",
                "rating": 5,
                "user_id": 6,
            },
            {
                "text": "It's the African elephant",
                "rating": 2,
                "user_id": 7,
            },
        ],
    },
]


TAGS = [
    {"id": "sapr", "text": 'Кафедра РК6 "САПР"', "color": "success"},
    {"id": "animal", "text": "Животные", "color": "danger"},
    {"id": "books", "text": "Книги", "color": "warning"},
    {"id": "it", "text": "IT и погромирование", "color": "info"},
    {"id": "cat", "text": "Кошки", "color": "info"},
]

POPULAR_TAGS = TAGS

BEST_MEMBERS = [
    USERS[5],
    USERS[1],
    USERS[2],
    USERS[3],
    USERS[4],
]
