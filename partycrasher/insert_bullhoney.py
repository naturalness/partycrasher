#!/usr/bin/env python

import os
import sys

REPOSITORY_ROUTE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(REPOSITORY_ROUTE)

import requests
import partycrasher.rest_client


# JSON aliases for Python literals.
true, false, null = True, False, None

# Created using http://www.json-generator.com/
# Has ints, nulls, bools, strings, arrays, and objects.

TEMPLATE = r'''
[
  '{{repeat(5, 7)}}',
  {
    database_id: '{{objectId()}}',
    index: '{{index()}}',
    guid: '{{guid()}}',
    isActive: '{{bool()}}',
    balance: '{{floating(1000, 4000, 2, "$0,0.00")}}',
    picture: 'http://placehold.it/32x32',
    age: '{{integer(20, 40)}}',
    eyeColor: '{{random("blue", "brown", "green")}}',
    name: '{{firstName()}} {{surname()}}',
    gender: '{{gender()}}',
    company: '{{company().toUpperCase()}}',
    email: '{{email()}}',
    phone: '+1 {{phone()}}',
    address: '{{integer(100, 999)}} {{street()}}, {{city()}}, {{state()}}, {{integer(100, 10000)}}',
    about: '{{lorem(1, "paragraphs")}}',
    registered: '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
    latitude: '{{floating(-90.000001, 90)}}',
    longitude: '{{floating(-180.000001, 180)}}',
    tags: [
      '{{repeat(7)}}',
      '{{lorem(1, "words")}}'
    ],
    stacktrace: [
      '{{repeat(5, 50)}}',
      {
        "arguments": [
          '{{repeat(1, 5)}}',
          '{{lorem(1, "words")}}'
        ],
        "function": '{{lorem(1)}}',
        "address": '{{integer(0x7ffffffff, 0xffffffff)}}'
      }
    ],
    friends: [
      '{{repeat(3)}}',
      {
        id: '{{index()}}',
        name: '{{firstName()}} {{surname()}}',
        foos: '{{null}}'
      }
    ],
    greeting: function (tags) {
      return 'Hello, ' + this.name + '! You have ' + tags.integer(1, 10) + ' unread messages.';
    },
    favoriteFruit: function (tags) {
      var fruits = ['apple', 'banana', 'strawberry'];
      return fruits[tags.integer(0, fruits.length - 1)];
    }
  }
]
'''


SAMPLE_REPORTS = [
    {
        "database_id": "5755b9c5dbce64268cd5dea9",
        "index": 0,
        "guid": "ea81f58e-121f-4772-8d22-7aad756ec1d0",
        "isActive": false,
        "balance": "$3,181.96",
        "picture": "http://placehold.it/32x32",
        "age": 21,
        "eyeColor": "blue",
        "name": "Rowe Miller",
        "gender": "male",
        "company": "QIAO",
        "email": "rowemiller@qiao.com",
        "phone": "+1 (921) 499-2178",
        "address": "454 Clifford Place, Colton, Illinois, 1610",
        "about": "Consectetur et duis laboris magna dolor ut sint. Duis ipsum cillum aliqua fugiat excepteur. Dolore excepteur commodo do aliqua ut ad pariatur eiusmod. Dolore occaecat mollit reprehenderit veniam aliqua sunt dolor sint sint non officia amet ad ullamco.\r\n",
        "registered": "2016-02-21T12:18:00 +07:00",
        "latitude": -54.120988,
        "longitude": 117.534995,
        "tags": [
            "nisi",
            "id",
            "velit",
            "aliqua",
            "labore",
            "dolore",
            "aliquip"
        ],
        "stacktrace": [
            {
                "arguments": [
                    "proident",
                    "excepteur",
                    "nisi"
                ],
                "function": "Culpa velit voluptate nulla ex consequat mollit ex veniam reprehenderit.",
                "address": 21578847446
            },
            {
                "arguments": [
                    "nostrud",
                    "adipisicing"
                ],
                "function": "Duis ea quis esse reprehenderit laboris id.",
                "address": 29116934687
            },
            {
                "arguments": [
                    "est",
                    "reprehenderit"
                ],
                "function": "Consequat laborum nulla fugiat minim tempor elit officia pariatur in eiusmod ex pariatur eiusmod enim.",
                "address": 6019143250
            },
            {
                "arguments": [
                    "fugiat",
                    "excepteur",
                    "mollit"
                ],
                "function": "Cupidatat nostrud nisi est ut duis deserunt proident commodo qui eiusmod pariatur nostrud velit.",
                "address": 32086545420
            },
            {
                "arguments": [
                    "enim",
                    "id",
                    "fugiat"
                ],
                "function": "Adipisicing cillum officia ea esse.",
                "address": 16493399948
            },
            {
                "arguments": [
                    "officia",
                    "fugiat",
                    "officia",
                    "id",
                    "ipsum"
                ],
                "function": "Do voluptate sint velit veniam laboris exercitation aute.",
                "address": 23625944604
            },
            {
                "arguments": [
                    "adipisicing",
                    "quis",
                    "fugiat"
                ],
                "function": "Nostrud voluptate laborum consectetur adipisicing quis culpa mollit.",
                "address": 6896323150
            },
            {
                "arguments": [
                    "laborum",
                    "laborum"
                ],
                "function": "Officia minim deserunt reprehenderit incididunt duis cupidatat mollit sit exercitation esse proident tempor sit labore.",
                "address": 25489011124
            },
            {
                "arguments": [
                    "consectetur"
                ],
                "function": "Excepteur ea laboris dolor ad esse ex irure dolore.",
                "address": 18625468816
            },
            {
                "arguments": [
                    "sint",
                    "ut"
                ],
                "function": "Labore anim officia velit amet incididunt duis dolor incididunt.",
                "address": 21072672672
            },
            {
                "arguments": [
                    "deserunt",
                    "sit"
                ],
                "function": "Excepteur qui in laboris aute reprehenderit incididunt excepteur sint sint dolore id.",
                "address": 24829068222
            },
            {
                "arguments": [
                    "aute",
                    "culpa",
                    "irure"
                ],
                "function": "Ex excepteur anim et Lorem ullamco aliquip do.",
                "address": 24224830559
            },
            {
                "arguments": [
                    "duis",
                    "consectetur",
                    "voluptate",
                    "sunt",
                    "commodo"
                ],
                "function": "Magna quis elit eu eiusmod sint laboris nostrud incididunt eiusmod cillum eiusmod dolore.",
                "address": 18066165385
            },
            {
                "arguments": [
                    "pariatur",
                    "nostrud",
                    "amet",
                    "eiusmod"
                ],
                "function": "Adipisicing proident irure aliqua fugiat consequat consequat cillum aute quis ut et et.",
                "address": 9709966107
            },
            {
                "arguments": [
                    "voluptate",
                    "sunt",
                    "deserunt",
                    "pariatur"
                ],
                "function": "Eu Lorem ullamco nisi exercitation sint.",
                "address": 16565712519
            },
            {
                "arguments": [
                    "reprehenderit",
                    "mollit",
                    "ipsum"
                ],
                "function": "Id excepteur adipisicing consectetur sunt officia elit aute anim esse commodo proident aliqua nostrud duis.",
                "address": 32507868916
            },
            {
                "arguments": [
                    "cupidatat",
                    "non",
                    "aliquip",
                    "qui"
                ],
                "function": "Elit amet nostrud culpa laborum ea.",
                "address": 5973563754
            },
            {
                "arguments": [
                    "ut",
                    "consectetur",
                    "magna"
                ],
                "function": "Nulla minim consequat consequat labore exercitation mollit fugiat Lorem cupidatat dolore.",
                "address": 15697102176
            },
            {
                "arguments": [
                    "elit",
                    "aliquip",
                    "eu",
                    "amet"
                ],
                "function": "Quis commodo sit dolor tempor non anim occaecat esse laboris nisi qui non sit.",
                "address": 4729184404
            },
            {
                "arguments": [
                    "aliquip",
                    "deserunt",
                    "consequat"
                ],
                "function": "Est incididunt incididunt mollit ipsum ipsum.",
                "address": 16455175706
            },
            {
                "arguments": [
                    "fugiat",
                    "commodo",
                    "sunt",
                    "officia"
                ],
                "function": "Quis veniam Lorem reprehenderit laborum ad reprehenderit proident ea irure.",
                "address": 33929309611
            },
            {
                "arguments": [
                    "ut",
                    "commodo"
                ],
                "function": "Exercitation mollit labore laborum ullamco anim velit eiusmod aliquip.",
                "address": 4697115121
            },
            {
                "arguments": [
                    "non",
                    "laboris"
                ],
                "function": "Minim Lorem ad consequat proident aute fugiat elit officia est enim nostrud id laboris.",
                "address": 32800113250
            },
            {
                "arguments": [
                    "culpa",
                    "nostrud",
                    "enim",
                    "velit",
                    "ad"
                ],
                "function": "Labore mollit dolore ut minim proident voluptate voluptate.",
                "address": 30889796685
            },
            {
                "arguments": [
                    "sint",
                    "elit"
                ],
                "function": "Lorem reprehenderit fugiat ullamco non do non officia anim mollit ipsum proident est ipsum ullamco.",
                "address": 7254330683
            },
            {
                "arguments": [
                    "sunt",
                    "deserunt",
                    "id"
                ],
                "function": "Magna qui pariatur laboris pariatur duis.",
                "address": 7518358916
            },
            {
                "arguments": [
                    "ut",
                    "ea",
                    "aute",
                    "duis"
                ],
                "function": "Ullamco excepteur eu labore ipsum nulla ullamco sunt.",
                "address": 12325192394
            },
            {
                "arguments": [
                    "est",
                    "incididunt"
                ],
                "function": "Deserunt ad laboris dolore voluptate non eu excepteur.",
                "address": 5982360919
            },
            {
                "arguments": [
                    "dolore",
                    "occaecat"
                ],
                "function": "Ipsum qui minim laboris enim ad id tempor.",
                "address": 33570767584
            },
            {
                "arguments": [
                    "amet"
                ],
                "function": "Excepteur Lorem magna non mollit qui Lorem pariatur ipsum consectetur exercitation velit cupidatat.",
                "address": 28566383223
            },
            {
                "arguments": [
                    "non",
                    "commodo"
                ],
                "function": "Labore consequat voluptate adipisicing excepteur occaecat.",
                "address": 17694153183
            },
            {
                "arguments": [
                    "ex",
                    "tempor",
                    "cupidatat",
                    "dolore",
                    "Lorem"
                ],
                "function": "Id deserunt ea consequat aliqua Lorem ea occaecat mollit enim est.",
                "address": 14726971903
            },
            {
                "arguments": [
                    "officia"
                ],
                "function": "Ipsum culpa id consequat dolor sit labore eiusmod sit pariatur officia.",
                "address": 5487238402
            },
            {
                "arguments": [
                    "sint",
                    "deserunt",
                    "tempor",
                    "mollit",
                    "cillum"
                ],
                "function": "Culpa reprehenderit qui duis do.",
                "address": 14215112247
            },
            {
                "arguments": [
                    "consectetur",
                    "laborum"
                ],
                "function": "Ex et esse excepteur ipsum sit ea reprehenderit consectetur ut.",
                "address": 13153845928
            }
        ],
        "friends": [
            {
                "id": 0,
                "name": "Nannie Wall",
                "foos": null
            },
            {
                "id": 1,
                "name": "Wanda Burch",
                "foos": null
            },
            {
                "id": 2,
                "name": "Lancaster Chaney",
                "foos": null
            }
        ],
        "greeting": "Hello, Rowe Miller! You have 7 unread messages.",
        "favoriteFruit": "apple"
    },
    {
        "database_id": "5755b9c5954ab31716169c11",
        "index": 1,
        "guid": "ed9513d5-1bc6-42d2-ba41-8cea27ff2ec0",
        "isActive": true,
        "balance": "$3,228.50",
        "picture": "http://placehold.it/32x32",
        "age": 24,
        "eyeColor": "brown",
        "name": "Brock Rasmussen",
        "gender": "male",
        "company": "ENDICIL",
        "email": "brockrasmussen@endicil.com",
        "phone": "+1 (840) 484-3507",
        "address": "343 Brightwater Avenue, Summertown, Alabama, 9657",
        "about": "Amet culpa cillum nostrud sint irure enim irure ut minim eu. Ea aliquip irure eiusmod adipisicing incididunt culpa commodo nulla. Laborum ut deserunt ullamco consectetur occaecat id amet fugiat duis minim nisi velit consequat ullamco. Irure incididunt sunt commodo cillum mollit non velit veniam tempor deserunt occaecat excepteur veniam. Consectetur nulla officia nostrud et est aute consequat aute deserunt minim ea Lorem. Labore ea minim tempor mollit. Minim ex exercitation cupidatat culpa aliquip amet aute.\r\n",
        "registered": "2015-09-03T06:53:26 +06:00",
        "latitude": 60.4909,
        "longitude": -163.25565,
        "tags": [
            "veniam",
            "amet",
            "laborum",
            "exercitation",
            "eiusmod",
            "deserunt",
            "laboris"
        ],
        "stacktrace": [
            {
                "arguments": [
                    "mollit",
                    "labore",
                    "proident",
                    "dolore",
                    "sit"
                ],
                "function": "Cupidatat commodo veniam fugiat ullamco magna anim nulla consectetur ut consectetur nostrud ut.",
                "address": 9515522041
            },
            {
                "arguments": [
                    "elit"
                ],
                "function": "Occaecat incididunt incididunt ipsum proident culpa aliquip occaecat aliqua magna reprehenderit minim in.",
                "address": 11750921230
            },
            {
                "arguments": [
                    "qui",
                    "esse"
                ],
                "function": "Id nulla fugiat non sunt do.",
                "address": 32953237392
            },
            {
                "arguments": [
                    "consequat"
                ],
                "function": "Duis ea irure ad reprehenderit in voluptate ipsum deserunt sit.",
                "address": 32806838896
            },
            {
                "arguments": [
                    "mollit",
                    "fugiat",
                    "velit",
                    "mollit",
                    "fugiat"
                ],
                "function": "Labore eiusmod officia ex ex sint veniam.",
                "address": 4605671021
            },
            {
                "arguments": [
                    "eu",
                    "excepteur",
                    "nostrud"
                ],
                "function": "In cillum tempor nisi ut ad ipsum adipisicing reprehenderit exercitation.",
                "address": 8731423963
            },
            {
                "arguments": [
                    "incididunt",
                    "est"
                ],
                "function": "Voluptate id id esse ullamco mollit dolor ea reprehenderit nulla sint veniam in esse tempor.",
                "address": 26509549630
            },
            {
                "arguments": [
                    "amet",
                    "laboris",
                    "ex"
                ],
                "function": "Cillum amet velit voluptate sint ut laboris labore aliqua mollit culpa do reprehenderit anim.",
                "address": 11340634538
            },
            {
                "arguments": [
                    "laboris"
                ],
                "function": "Magna ut qui reprehenderit ea non aliquip eiusmod irure fugiat cupidatat laborum nulla laborum non.",
                "address": 15394922563
            },
            {
                "arguments": [
                    "officia",
                    "consectetur",
                    "ut",
                    "eu"
                ],
                "function": "Qui nisi aliqua officia aliquip eu anim.",
                "address": 14099348715
            },
            {
                "arguments": [
                    "proident",
                    "do",
                    "qui",
                    "laboris",
                    "cillum"
                ],
                "function": "Ut id consectetur elit nisi dolore aliquip.",
                "address": 5264316970
            },
            {
                "arguments": [
                    "minim",
                    "cupidatat"
                ],
                "function": "Pariatur officia commodo sint minim pariatur.",
                "address": 31903445580
            },
            {
                "arguments": [
                    "sunt",
                    "qui",
                    "fugiat",
                    "incididunt",
                    "non"
                ],
                "function": "Commodo occaecat duis ea cillum.",
                "address": 15331166821
            },
            {
                "arguments": [
                    "Lorem",
                    "anim",
                    "minim"
                ],
                "function": "Irure consequat mollit elit consequat ipsum veniam.",
                "address": 25122117652
            },
            {
                "arguments": [
                    "non",
                    "do"
                ],
                "function": "Commodo reprehenderit fugiat proident labore deserunt ad ullamco pariatur.",
                "address": 9148616114
            },
            {
                "arguments": [
                    "ullamco",
                    "ipsum"
                ],
                "function": "Esse deserunt ullamco ut id.",
                "address": 26293478794
            },
            {
                "arguments": [
                    "dolor"
                ],
                "function": "Officia sint tempor dolor id exercitation est non.",
                "address": 9165001764
            },
            {
                "arguments": [
                    "eiusmod",
                    "dolore",
                    "elit",
                    "tempor"
                ],
                "function": "Laboris dolore nulla qui do dolor.",
                "address": 22535364987
            },
            {
                "arguments": [
                    "ut"
                ],
                "function": "Ad fugiat culpa sunt occaecat commodo irure sint elit quis proident voluptate nostrud enim et.",
                "address": 22057201699
            },
            {
                "arguments": [
                    "dolore"
                ],
                "function": "Laborum ut exercitation duis proident.",
                "address": 31033921588
            },
            {
                "arguments": [
                    "ea"
                ],
                "function": "Dolore laboris proident aliqua est.",
                "address": 7368437624
            },
            {
                "arguments": [
                    "ipsum",
                    "dolor"
                ],
                "function": "Laboris nostrud consectetur incididunt eu pariatur sit culpa ex occaecat voluptate ad nulla.",
                "address": 11338699599
            },
            {
                "arguments": [
                    "cillum",
                    "proident",
                    "dolor",
                    "et",
                    "enim"
                ],
                "function": "Pariatur tempor ad exercitation non Lorem nostrud proident ut.",
                "address": 26270043609
            },
            {
                "arguments": [
                    "culpa"
                ],
                "function": "Laboris tempor culpa ut dolor ea veniam excepteur eiusmod cillum consequat mollit sit eiusmod officia.",
                "address": 7337107196
            },
            {
                "arguments": [
                    "dolore",
                    "anim"
                ],
                "function": "Reprehenderit est voluptate anim mollit excepteur culpa aliqua.",
                "address": 8552587396
            },
            {
                "arguments": [
                    "id",
                    "nulla"
                ],
                "function": "Duis incididunt id consectetur labore id eu sint excepteur deserunt sunt.",
                "address": 15835978376
            },
            {
                "arguments": [
                    "magna",
                    "esse",
                    "magna"
                ],
                "function": "Anim dolor id irure sint consectetur dolore id consequat deserunt ex consectetur minim qui.",
                "address": 13160726167
            },
            {
                "arguments": [
                    "enim"
                ],
                "function": "Velit in dolore nostrud pariatur fugiat est veniam commodo laborum irure eiusmod.",
                "address": 33275013885
            },
            {
                "arguments": [
                    "aliquip",
                    "id",
                    "officia"
                ],
                "function": "Sit amet minim ipsum in proident.",
                "address": 11081720169
            },
            {
                "arguments": [
                    "officia",
                    "quis"
                ],
                "function": "Voluptate laboris proident deserunt adipisicing.",
                "address": 21024603980
            },
            {
                "arguments": [
                    "nostrud"
                ],
                "function": "Mollit velit veniam ipsum commodo ea eu sit consequat adipisicing mollit deserunt non magna.",
                "address": 24998665045
            },
            {
                "arguments": [
                    "esse"
                ],
                "function": "Do labore irure quis nostrud minim id fugiat aliqua sint nostrud ut pariatur fugiat.",
                "address": 8836178793
            },
            {
                "arguments": [
                    "irure",
                    "eu"
                ],
                "function": "Consequat sit adipisicing cillum non anim excepteur id eiusmod irure.",
                "address": 16998152770
            },
            {
                "arguments": [
                    "veniam",
                    "duis",
                    "pariatur",
                    "cupidatat",
                    "dolor"
                ],
                "function": "Mollit cillum elit magna ullamco voluptate ullamco ex ea elit ut sunt voluptate.",
                "address": 6021954925
            },
            {
                "arguments": [
                    "pariatur"
                ],
                "function": "Aute nisi enim pariatur reprehenderit magna et ullamco.",
                "address": 29105655701
            },
            {
                "arguments": [
                    "id",
                    "veniam",
                    "veniam",
                    "in"
                ],
                "function": "Nulla nulla commodo veniam ea aute.",
                "address": 33334918198
            },
            {
                "arguments": [
                    "veniam",
                    "aute",
                    "nulla",
                    "quis"
                ],
                "function": "Incididunt culpa aliquip culpa exercitation do.",
                "address": 15853425922
            },
            {
                "arguments": [
                    "ut",
                    "enim",
                    "mollit",
                    "adipisicing"
                ],
                "function": "Magna non nostrud incididunt cupidatat.",
                "address": 12807844067
            },
            {
                "arguments": [
                    "eiusmod",
                    "voluptate",
                    "velit"
                ],
                "function": "Aliquip anim dolore qui dolor sunt minim consectetur qui minim magna qui cupidatat veniam tempor.",
                "address": 19918427354
            },
            {
                "arguments": [
                    "veniam",
                    "adipisicing",
                    "sint",
                    "ad",
                    "adipisicing"
                ],
                "function": "Ad elit cupidatat esse in cupidatat aliquip.",
                "address": 14785592611
            },
            {
                "arguments": [
                    "fugiat",
                    "irure",
                    "nisi"
                ],
                "function": "Do irure cupidatat quis commodo excepteur labore.",
                "address": 27167318720
            }
        ],
        "friends": [
            {
                "id": 0,
                "name": "Latoya Nash",
                "foos": null
            },
            {
                "id": 1,
                "name": "Natalie Allen",
                "foos": null
            },
            {
                "id": 2,
                "name": "Freida Rhodes",
                "foos": null
            }
        ],
        "greeting": "Hello, Brock Rasmussen! You have 7 unread messages.",
        "favoriteFruit": "apple"
    },
    {
        "database_id": "5755b9c5f7b7b642ab2d29e3",
        "index": 2,
        "guid": "61cc6d19-ec48-4041-806b-22c6fd0e3e62",
        "isActive": true,
        "balance": "$1,791.15",
        "picture": "http://placehold.it/32x32",
        "age": 29,
        "eyeColor": "green",
        "name": "Deena Doyle",
        "gender": "female",
        "company": "DEVILTOE",
        "email": "deenadoyle@deviltoe.com",
        "phone": "+1 (991) 450-3569",
        "address": "529 Joralemon Street, Alden, Idaho, 3344",
        "about": "Officia labore tempor velit culpa est cillum tempor cillum deserunt aliquip duis proident eiusmod. Qui consectetur officia sunt laboris sint. Irure incididunt irure magna dolor ipsum laborum voluptate cupidatat sit. In consectetur irure exercitation tempor velit aute minim incididunt esse velit. Quis nulla occaecat laboris consequat proident. Officia reprehenderit non do do.\r\n",
        "registered": "2015-05-10T12:20:25 +06:00",
        "latitude": -73.413255,
        "longitude": 169.320097,
        "tags": [
            "eu",
            "consequat",
            "officia",
            "sunt",
            "excepteur",
            "sint",
            "officia"
        ],
        "stacktrace": [
            {
                "arguments": [
                    "esse",
                    "duis",
                    "dolor",
                    "qui"
                ],
                "function": "Anim et laboris non laboris sunt occaecat cupidatat et duis pariatur non veniam cillum.",
                "address": 12300991523
            },
            {
                "arguments": [
                    "eiusmod",
                    "sint",
                    "labore",
                    "amet"
                ],
                "function": "Laborum exercitation irure nisi consectetur esse proident laborum deserunt ut ipsum dolore aliqua excepteur.",
                "address": 28039416757
            },
            {
                "arguments": [
                    "qui",
                    "id",
                    "dolor"
                ],
                "function": "Consequat qui velit elit duis.",
                "address": 28092442458
            },
            {
                "arguments": [
                    "veniam",
                    "eu",
                    "elit",
                    "excepteur"
                ],
                "function": "Minim sit commodo dolor sunt cupidatat quis irure velit.",
                "address": 31855671292
            },
            {
                "arguments": [
                    "in"
                ],
                "function": "Laborum cupidatat sunt in fugiat quis id officia commodo non mollit eiusmod exercitation ipsum.",
                "address": 9945381492
            },
            {
                "arguments": [
                    "id",
                    "elit",
                    "cillum",
                    "ex"
                ],
                "function": "Officia quis tempor minim eiusmod id ullamco pariatur.",
                "address": 27729938399
            },
            {
                "arguments": [
                    "velit",
                    "incididunt",
                    "esse",
                    "pariatur"
                ],
                "function": "Culpa magna ad consequat laboris fugiat labore aute incididunt qui laborum commodo fugiat.",
                "address": 5477254748
            },
            {
                "arguments": [
                    "nostrud"
                ],
                "function": "Mollit pariatur tempor tempor velit cupidatat anim labore fugiat.",
                "address": 28534642240
            },
            {
                "arguments": [
                    "sit",
                    "aute",
                    "enim",
                    "aliqua",
                    "eu"
                ],
                "function": "Sint quis Lorem dolor velit reprehenderit in adipisicing nisi dolore excepteur enim consequat.",
                "address": 6496811007
            },
            {
                "arguments": [
                    "incididunt",
                    "mollit",
                    "nulla",
                    "dolore"
                ],
                "function": "Ex duis nulla dolore sint adipisicing id do.",
                "address": 17114780756
            },
            {
                "arguments": [
                    "veniam",
                    "aute",
                    "eu"
                ],
                "function": "Commodo exercitation et minim dolore velit excepteur ipsum cillum in culpa do eiusmod tempor incididunt.",
                "address": 13455540763
            },
            {
                "arguments": [
                    "est",
                    "laborum",
                    "aute"
                ],
                "function": "Exercitation elit eu amet Lorem sit sint amet laborum nostrud commodo.",
                "address": 6033540801
            },
            {
                "arguments": [
                    "sint",
                    "laboris",
                    "incididunt",
                    "ipsum"
                ],
                "function": "Exercitation et velit officia eu nisi tempor dolore esse aute dolor commodo dolore.",
                "address": 24415261838
            },
            {
                "arguments": [
                    "laborum",
                    "excepteur",
                    "nisi"
                ],
                "function": "Id elit Lorem ut labore dolor nisi.",
                "address": 5836169766
            },
            {
                "arguments": [
                    "ex",
                    "id"
                ],
                "function": "Ex in anim exercitation in consequat nulla culpa officia voluptate velit voluptate occaecat.",
                "address": 15595655363
            },
            {
                "arguments": [
                    "elit",
                    "nisi",
                    "amet",
                    "culpa"
                ],
                "function": "Incididunt mollit aliqua qui laboris fugiat eu voluptate non minim voluptate commodo elit.",
                "address": 21131381750
            },
            {
                "arguments": [
                    "eu"
                ],
                "function": "Magna proident velit ullamco incididunt consequat irure quis Lorem reprehenderit non sunt commodo.",
                "address": 23360292119
            },
            {
                "arguments": [
                    "elit",
                    "eiusmod",
                    "eiusmod",
                    "sint",
                    "veniam"
                ],
                "function": "In cupidatat adipisicing irure ut aliquip cupidatat eiusmod nulla nisi enim aliquip ad.",
                "address": 33302480857
            },
            {
                "arguments": [
                    "ullamco",
                    "aliquip",
                    "occaecat",
                    "consequat",
                    "tempor"
                ],
                "function": "Do sit cillum labore nostrud.",
                "address": 30687363969
            },
            {
                "arguments": [
                    "nulla"
                ],
                "function": "Sint officia sit Lorem nostrud nulla non laboris proident eu Lorem reprehenderit elit.",
                "address": 8931671516
            },
            {
                "arguments": [
                    "aute",
                    "dolore"
                ],
                "function": "Incididunt nisi ipsum aute labore ipsum eu.",
                "address": 16711481129
            },
            {
                "arguments": [
                    "ut",
                    "ea",
                    "dolore",
                    "consequat",
                    "in"
                ],
                "function": "Mollit laborum anim Lorem cillum id voluptate elit veniam magna.",
                "address": 23294517553
            },
            {
                "arguments": [
                    "esse",
                    "quis",
                    "sunt",
                    "exercitation"
                ],
                "function": "Commodo amet deserunt enim in nulla culpa.",
                "address": 25227412316
            },
            {
                "arguments": [
                    "quis"
                ],
                "function": "Sit consequat cillum duis dolor mollit fugiat commodo excepteur nisi adipisicing.",
                "address": 23092151351
            },
            {
                "arguments": [
                    "voluptate",
                    "incididunt",
                    "sint",
                    "ut"
                ],
                "function": "Anim sunt laborum voluptate culpa consequat et voluptate ea et qui non.",
                "address": 17502415111
            },
            {
                "arguments": [
                    "ut",
                    "mollit"
                ],
                "function": "Irure velit id est proident laboris nostrud esse culpa commodo aute amet in duis ut.",
                "address": 33934191954
            },
            {
                "arguments": [
                    "ut"
                ],
                "function": "Voluptate irure sit do exercitation nostrud fugiat et ut elit minim.",
                "address": 15838243688
            },
            {
                "arguments": [
                    "eiusmod"
                ],
                "function": "Cupidatat dolor labore et ad consectetur Lorem proident non proident veniam veniam fugiat.",
                "address": 19456784300
            },
            {
                "arguments": [
                    "occaecat",
                    "proident",
                    "nostrud"
                ],
                "function": "Consectetur irure ipsum excepteur nostrud et labore amet adipisicing velit mollit minim.",
                "address": 31370971431
            },
            {
                "arguments": [
                    "tempor"
                ],
                "function": "Enim proident et sunt officia incididunt minim aliquip cillum in labore qui nostrud anim laboris.",
                "address": 8491506973
            },
            {
                "arguments": [
                    "ut",
                    "exercitation"
                ],
                "function": "Consectetur esse ea qui dolor eiusmod dolore ea fugiat pariatur reprehenderit amet sit.",
                "address": 16522198554
            },
            {
                "arguments": [
                    "laborum"
                ],
                "function": "Ut in proident eu non occaecat.",
                "address": 21371495534
            },
            {
                "arguments": [
                    "occaecat",
                    "proident",
                    "velit",
                    "ad"
                ],
                "function": "Ipsum velit sit consectetur aute exercitation.",
                "address": 13484592159
            },
            {
                "arguments": [
                    "pariatur"
                ],
                "function": "Exercitation aute commodo ipsum enim consectetur.",
                "address": 19526676872
            },
            {
                "arguments": [
                    "incididunt",
                    "occaecat",
                    "ut",
                    "anim",
                    "esse"
                ],
                "function": "Enim minim aute Lorem commodo.",
                "address": 25827405728
            },
            {
                "arguments": [
                    "sunt",
                    "magna"
                ],
                "function": "Veniam laboris mollit ullamco excepteur nisi ipsum do et velit adipisicing deserunt dolor laborum.",
                "address": 25421531903
            },
            {
                "arguments": [
                    "ea",
                    "occaecat"
                ],
                "function": "In sit minim elit est excepteur in excepteur fugiat.",
                "address": 9791056528
            },
            {
                "arguments": [
                    "dolore"
                ],
                "function": "Occaecat sint aliquip est do.",
                "address": 11783313111
            },
            {
                "arguments": [
                    "nisi",
                    "non",
                    "anim",
                    "consectetur"
                ],
                "function": "Deserunt aute aliqua cupidatat voluptate aute amet sunt elit duis cillum aliquip ea dolore.",
                "address": 4332136828
            },
            {
                "arguments": [
                    "commodo"
                ],
                "function": "Velit esse exercitation ullamco amet anim et.",
                "address": 7995150529
            },
            {
                "arguments": [
                    "ipsum",
                    "voluptate"
                ],
                "function": "Sint nostrud nulla magna id laborum cupidatat tempor cupidatat tempor irure minim irure nostrud.",
                "address": 25679503220
            },
            {
                "arguments": [
                    "incididunt",
                    "exercitation",
                    "magna"
                ],
                "function": "Magna tempor laborum amet et laboris.",
                "address": 6097225443
            },
            {
                "arguments": [
                    "fugiat",
                    "pariatur",
                    "sunt",
                    "officia"
                ],
                "function": "Nisi dolore id aliquip adipisicing excepteur dolore aliqua duis officia minim ad mollit sint.",
                "address": 24686061017
            },
            {
                "arguments": [
                    "est",
                    "nulla",
                    "anim"
                ],
                "function": "Amet amet fugiat eiusmod esse deserunt ad consectetur fugiat mollit sunt consectetur excepteur laboris eu.",
                "address": 26687480586
            }
        ],
        "friends": [
            {
                "id": 0,
                "name": "Mavis Logan",
                "foos": null
            },
            {
                "id": 1,
                "name": "Alyce Jacobson",
                "foos": null
            },
            {
                "id": 2,
                "name": "Hansen Harmon",
                "foos": null
            }
        ],
        "greeting": "Hello, Deena Doyle! You have 4 unread messages.",
        "favoriteFruit": "strawberry"
    },
    {
        "database_id": "5755b9c57bfbd27283b28847",
        "index": 3,
        "guid": "f4f0b5af-92e5-4200-9522-934e20d63ad5",
        "isActive": true,
        "balance": "$1,366.60",
        "picture": "http://placehold.it/32x32",
        "age": 39,
        "eyeColor": "green",
        "name": "Mccarty Bennett",
        "gender": "male",
        "company": "XYMONK",
        "email": "mccartybennett@xymonk.com",
        "phone": "+1 (805) 486-2337",
        "address": "351 College Place, Bridgetown, West Virginia, 1066",
        "about": "Quis laborum id laboris et enim aliqua cupidatat qui ea quis. Occaecat Lorem eu non voluptate proident. Laborum veniam ut consequat excepteur pariatur deserunt Lorem irure ipsum in culpa. Duis in dolore excepteur amet consectetur fugiat consectetur. Anim laborum occaecat voluptate minim pariatur consectetur aliquip dolore veniam amet. Deserunt irure pariatur veniam ipsum aliqua officia et eu.\r\n",
        "registered": "2015-12-04T02:06:52 +07:00",
        "latitude": 2.918512,
        "longitude": 61.448723,
        "tags": [
            "nulla",
            "amet",
            "Lorem",
            "nisi",
            "ea",
            "duis",
            "do"
        ],
        "stacktrace": [
            {
                "arguments": [
                    "deserunt",
                    "proident",
                    "culpa",
                    "anim",
                    "consectetur"
                ],
                "function": "Magna ad velit veniam nostrud excepteur eu quis ipsum id aute Lorem dolor duis ut.",
                "address": 24599601237
            },
            {
                "arguments": [
                    "sunt",
                    "laboris",
                    "dolor",
                    "aute"
                ],
                "function": "Excepteur voluptate enim ut officia laborum minim sit esse.",
                "address": 33678600766
            },
            {
                "arguments": [
                    "officia",
                    "voluptate"
                ],
                "function": "Lorem velit dolore sunt irure Lorem nulla fugiat id aliquip sunt quis.",
                "address": 4372861782
            },
            {
                "arguments": [
                    "culpa"
                ],
                "function": "Deserunt non nostrud velit ipsum exercitation cillum ad tempor id reprehenderit dolore sit sunt elit.",
                "address": 9059962894
            },
            {
                "arguments": [
                    "consectetur",
                    "consequat"
                ],
                "function": "Incididunt minim culpa proident elit Lorem fugiat culpa dolor incididunt occaecat.",
                "address": 31274215548
            },
            {
                "arguments": [
                    "nisi",
                    "ut"
                ],
                "function": "Mollit ut sit adipisicing commodo sunt qui.",
                "address": 6030943205
            },
            {
                "arguments": [
                    "qui",
                    "do",
                    "ipsum"
                ],
                "function": "Culpa officia id in irure culpa aliquip exercitation.",
                "address": 10250474165
            },
            {
                "arguments": [
                    "commodo",
                    "mollit",
                    "magna",
                    "officia",
                    "ipsum"
                ],
                "function": "Eu anim proident incididunt nisi cillum amet culpa tempor.",
                "address": 32434595088
            },
            {
                "arguments": [
                    "sunt",
                    "sint"
                ],
                "function": "Id aliqua ea nisi ullamco ex commodo occaecat ut laborum eu.",
                "address": 25614534683
            },
            {
                "arguments": [
                    "in",
                    "tempor",
                    "tempor",
                    "sunt"
                ],
                "function": "Elit aliquip cupidatat veniam dolor minim elit laboris officia ullamco.",
                "address": 16928678752
            },
            {
                "arguments": [
                    "exercitation"
                ],
                "function": "Est elit et do non Lorem ea voluptate.",
                "address": 11785655618
            },
            {
                "arguments": [
                    "nulla",
                    "commodo"
                ],
                "function": "In quis officia Lorem sint dolore consequat sit commodo officia veniam ullamco ex fugiat.",
                "address": 18458841470
            },
            {
                "arguments": [
                    "ad",
                    "laboris"
                ],
                "function": "Ipsum veniam consectetur do veniam non eu.",
                "address": 26194883297
            },
            {
                "arguments": [
                    "pariatur",
                    "cillum",
                    "ad"
                ],
                "function": "Cillum labore esse enim eu.",
                "address": 27355123972
            },
            {
                "arguments": [
                    "id",
                    "consectetur"
                ],
                "function": "In laboris ad duis exercitation dolor.",
                "address": 29619308271
            },
            {
                "arguments": [
                    "esse",
                    "consequat"
                ],
                "function": "Cillum adipisicing eu Lorem magna Lorem qui aliqua eiusmod voluptate laboris ea ullamco proident occaecat.",
                "address": 18113046818
            },
            {
                "arguments": [
                    "nulla"
                ],
                "function": "Tempor duis duis velit nostrud.",
                "address": 22965835257
            },
            {
                "arguments": [
                    "irure",
                    "fugiat",
                    "occaecat"
                ],
                "function": "Commodo in anim est ullamco mollit non.",
                "address": 32076329845
            },
            {
                "arguments": [
                    "velit",
                    "ullamco"
                ],
                "function": "Officia ex anim in elit duis fugiat occaecat nulla culpa dolore consectetur consectetur ea laborum.",
                "address": 22898689790
            },
            {
                "arguments": [
                    "ad",
                    "ullamco",
                    "sint"
                ],
                "function": "Ullamco dolore amet nostrud voluptate non officia aliquip aliquip fugiat tempor.",
                "address": 22573725355
            },
            {
                "arguments": [
                    "consectetur",
                    "qui",
                    "in",
                    "fugiat",
                    "consequat"
                ],
                "function": "Aute adipisicing ut do veniam.",
                "address": 20053065779
            },
            {
                "arguments": [
                    "incididunt",
                    "officia",
                    "anim",
                    "sit",
                    "proident"
                ],
                "function": "Exercitation elit elit in veniam commodo.",
                "address": 19740770071
            },
            {
                "arguments": [
                    "laborum",
                    "consectetur",
                    "sint",
                    "occaecat",
                    "velit"
                ],
                "function": "Ad cupidatat do ex magna aliqua minim.",
                "address": 9127813947
            },
            {
                "arguments": [
                    "irure",
                    "reprehenderit",
                    "et",
                    "ipsum",
                    "ea"
                ],
                "function": "Commodo ullamco exercitation pariatur cillum.",
                "address": 20297208522
            },
            {
                "arguments": [
                    "sint",
                    "irure"
                ],
                "function": "Duis qui voluptate cupidatat esse magna do esse Lorem excepteur pariatur aliqua occaecat non mollit.",
                "address": 21842386587
            },
            {
                "arguments": [
                    "tempor"
                ],
                "function": "Esse dolore ex cillum velit ex mollit cupidatat occaecat ipsum labore fugiat qui irure.",
                "address": 11281836975
            },
            {
                "arguments": [
                    "dolore",
                    "fugiat",
                    "commodo"
                ],
                "function": "Nulla dolor veniam tempor enim mollit.",
                "address": 18772275244
            },
            {
                "arguments": [
                    "mollit",
                    "culpa",
                    "adipisicing",
                    "sint"
                ],
                "function": "Nisi excepteur nulla reprehenderit aute aute magna ullamco mollit.",
                "address": 27157434463
            },
            {
                "arguments": [
                    "commodo"
                ],
                "function": "Ullamco dolore irure do aliqua consequat commodo nisi quis et amet anim non.",
                "address": 15286930210
            },
            {
                "arguments": [
                    "consectetur",
                    "duis",
                    "excepteur",
                    "deserunt"
                ],
                "function": "Ipsum nostrud sunt elit consequat ex sunt ad duis.",
                "address": 14593342855
            },
            {
                "arguments": [
                    "aliqua"
                ],
                "function": "Proident nisi anim ad ad aliqua.",
                "address": 16690385606
            },
            {
                "arguments": [
                    "ex"
                ],
                "function": "Adipisicing minim ad et incididunt.",
                "address": 34064032966
            },
            {
                "arguments": [
                    "laboris",
                    "reprehenderit"
                ],
                "function": "Duis incididunt do esse do aliquip do magna laborum laborum nostrud labore sunt commodo.",
                "address": 21659534473
            },
            {
                "arguments": [
                    "ut",
                    "aliqua",
                    "elit",
                    "commodo"
                ],
                "function": "Sint labore enim sunt velit reprehenderit consectetur minim.",
                "address": 19511066286
            },
            {
                "arguments": [
                    "ipsum",
                    "labore"
                ],
                "function": "In mollit voluptate voluptate laboris nostrud laboris adipisicing ipsum exercitation ut.",
                "address": 21219556708
            },
            {
                "arguments": [
                    "tempor",
                    "cillum",
                    "aute"
                ],
                "function": "Tempor commodo consequat duis exercitation enim do amet mollit exercitation Lorem mollit mollit minim quis.",
                "address": 8977428511
            },
            {
                "arguments": [
                    "cupidatat",
                    "laboris",
                    "velit",
                    "laborum",
                    "qui"
                ],
                "function": "Ex sunt esse irure deserunt ipsum quis voluptate veniam.",
                "address": 29853939353
            },
            {
                "arguments": [
                    "aliqua",
                    "est",
                    "adipisicing",
                    "pariatur",
                    "labore"
                ],
                "function": "Ipsum non cupidatat esse qui officia voluptate.",
                "address": 11467645300
            },
            {
                "arguments": [
                    "nisi",
                    "quis",
                    "ipsum",
                    "ipsum"
                ],
                "function": "Irure incididunt esse magna eiusmod quis pariatur.",
                "address": 11839009885
            },
            {
                "arguments": [
                    "incididunt",
                    "ex",
                    "aute",
                    "ullamco"
                ],
                "function": "Proident esse irure id pariatur reprehenderit excepteur voluptate culpa et cillum in velit.",
                "address": 20847364057
            },
            {
                "arguments": [
                    "do",
                    "ullamco",
                    "sunt"
                ],
                "function": "Ullamco proident velit quis reprehenderit aliquip adipisicing exercitation deserunt mollit.",
                "address": 34319962619
            }
        ],
        "friends": [
            {
                "id": 0,
                "name": "Acevedo Ward",
                "foos": null
            },
            {
                "id": 1,
                "name": "Valerie Jarvis",
                "foos": null
            },
            {
                "id": 2,
                "name": "Judy Bentley",
                "foos": null
            }
        ],
        "greeting": "Hello, Mccarty Bennett! You have 6 unread messages.",
        "favoriteFruit": "banana"
    },
    {
        "database_id": "5755b9c5c94090160e8f698d",
        "index": 4,
        "guid": "cab2ee5e-1b4a-427b-96d6-25b40ecb8dea",
        "isActive": true,
        "balance": "$3,884.93",
        "picture": "http://placehold.it/32x32",
        "age": 27,
        "eyeColor": "green",
        "name": "Dionne Maldonado",
        "gender": "female",
        "company": "TERAPRENE",
        "email": "dionnemaldonado@teraprene.com",
        "phone": "+1 (874) 414-3744",
        "address": "721 Shale Street, Coventry, Wyoming, 190",
        "about": "Sint anim ex laboris ad in quis elit exercitation fugiat culpa non. Consequat esse cillum mollit culpa labore aliqua. Ex fugiat incididunt veniam ex officia fugiat ullamco sint. Elit amet dolor fugiat dolore. Cillum eiusmod est irure mollit nisi enim aliqua voluptate in. Proident deserunt quis magna dolor tempor. Aliquip Lorem ullamco pariatur est.\r\n",
        "registered": "2014-03-18T07:18:25 +06:00",
        "latitude": -17.472187,
        "longitude": -162.239293,
        "tags": [
            "fugiat",
            "tempor",
            "ipsum",
            "do",
            "nisi",
            "ad",
            "elit"
        ],
        "stacktrace": [
            {
                "arguments": [
                    "tempor"
                ],
                "function": "Irure exercitation aliqua laborum ad aute ipsum.",
                "address": 7381907929
            },
            {
                "arguments": [
                    "incididunt",
                    "sint",
                    "minim",
                    "irure"
                ],
                "function": "Velit ex veniam aliquip eu laboris aute.",
                "address": 32264636781
            },
            {
                "arguments": [
                    "in",
                    "ut",
                    "veniam",
                    "aliqua",
                    "aute"
                ],
                "function": "Do laborum eiusmod eu amet consectetur do voluptate laborum.",
                "address": 28031423401
            },
            {
                "arguments": [
                    "id",
                    "in",
                    "dolor",
                    "eu",
                    "mollit"
                ],
                "function": "Reprehenderit voluptate dolore quis esse sit laborum.",
                "address": 30608792422
            },
            {
                "arguments": [
                    "ea"
                ],
                "function": "Officia elit fugiat minim mollit aliqua tempor ex velit pariatur.",
                "address": 15386675090
            },
            {
                "arguments": [
                    "irure",
                    "sit",
                    "id",
                    "est",
                    "cillum"
                ],
                "function": "Qui aliqua reprehenderit excepteur voluptate magna eu commodo nostrud deserunt nisi.",
                "address": 6544755684
            },
            {
                "arguments": [
                    "sint",
                    "irure",
                    "excepteur",
                    "nostrud",
                    "exercitation"
                ],
                "function": "Excepteur deserunt enim fugiat anim dolore.",
                "address": 4375428021
            },
            {
                "arguments": [
                    "quis",
                    "ad",
                    "laborum",
                    "nulla",
                    "tempor"
                ],
                "function": "Anim tempor qui non irure ullamco enim minim.",
                "address": 12789399035
            },
            {
                "arguments": [
                    "qui",
                    "ea",
                    "non"
                ],
                "function": "Sunt dolore ipsum mollit sit culpa ullamco dolore exercitation cupidatat aute nulla esse culpa.",
                "address": 10534031946
            },
            {
                "arguments": [
                    "mollit",
                    "exercitation",
                    "dolor",
                    "tempor",
                    "commodo"
                ],
                "function": "Adipisicing quis qui esse labore commodo ad proident ea ipsum cillum ex ullamco tempor.",
                "address": 27752339902
            },
            {
                "arguments": [
                    "laborum"
                ],
                "function": "Laborum qui laboris nisi enim sunt.",
                "address": 25722745728
            },
            {
                "arguments": [
                    "veniam",
                    "laboris",
                    "mollit"
                ],
                "function": "Adipisicing est id dolore pariatur excepteur officia quis nisi adipisicing.",
                "address": 27445480894
            },
            {
                "arguments": [
                    "sint",
                    "velit"
                ],
                "function": "In proident sunt laboris elit.",
                "address": 22792867472
            },
            {
                "arguments": [
                    "Lorem",
                    "tempor",
                    "incididunt"
                ],
                "function": "Eu sint non labore cupidatat enim.",
                "address": 30848760926
            },
            {
                "arguments": [
                    "enim"
                ],
                "function": "Nisi duis velit exercitation minim dolore ullamco eu excepteur laborum pariatur ipsum.",
                "address": 14512695996
            },
            {
                "arguments": [
                    "dolor",
                    "exercitation",
                    "aliqua",
                    "qui"
                ],
                "function": "In anim eiusmod exercitation aliquip aute sunt sint quis nostrud labore.",
                "address": 21544027542
            },
            {
                "arguments": [
                    "irure"
                ],
                "function": "Ad incididunt ut ad fugiat tempor.",
                "address": 15024380802
            },
            {
                "arguments": [
                    "in"
                ],
                "function": "Labore est ex voluptate nisi do ex.",
                "address": 32857216793
            },
            {
                "arguments": [
                    "mollit",
                    "commodo",
                    "qui",
                    "eu"
                ],
                "function": "Do pariatur deserunt ex voluptate officia eiusmod commodo tempor occaecat.",
                "address": 5227769981
            },
            {
                "arguments": [
                    "consectetur",
                    "enim",
                    "qui"
                ],
                "function": "Do quis esse culpa adipisicing dolore nulla.",
                "address": 21311940556
            },
            {
                "arguments": [
                    "irure",
                    "amet",
                    "do"
                ],
                "function": "Laboris anim fugiat incididunt ullamco pariatur nisi culpa est mollit amet.",
                "address": 33003627080
            },
            {
                "arguments": [
                    "sunt"
                ],
                "function": "Tempor reprehenderit sunt pariatur non non.",
                "address": 27728351050
            },
            {
                "arguments": [
                    "eu"
                ],
                "function": "Aute adipisicing duis nulla ex.",
                "address": 29277565418
            },
            {
                "arguments": [
                    "culpa",
                    "ad"
                ],
                "function": "Sint qui officia irure nisi aliquip velit.",
                "address": 34101425760
            },
            {
                "arguments": [
                    "cupidatat"
                ],
                "function": "Aliquip consectetur cillum est nostrud reprehenderit aliqua adipisicing Lorem.",
                "address": 22442369609
            },
            {
                "arguments": [
                    "duis",
                    "ipsum"
                ],
                "function": "Elit et nostrud eiusmod ipsum tempor velit laborum commodo quis minim reprehenderit esse.",
                "address": 28467502492
            },
            {
                "arguments": [
                    "labore",
                    "anim",
                    "aute",
                    "minim"
                ],
                "function": "Anim nulla qui ut sint occaecat anim tempor qui voluptate voluptate adipisicing duis tempor ad.",
                "address": 4889796647
            },
            {
                "arguments": [
                    "consectetur"
                ],
                "function": "Elit nulla et ex tempor ex magna pariatur consequat nisi.",
                "address": 29538587172
            },
            {
                "arguments": [
                    "ipsum"
                ],
                "function": "Duis duis reprehenderit consectetur Lorem reprehenderit eu deserunt qui consequat irure.",
                "address": 26373228835
            },
            {
                "arguments": [
                    "ut"
                ],
                "function": "Id ea cillum pariatur consectetur minim.",
                "address": 11936311868
            },
            {
                "arguments": [
                    "dolor",
                    "voluptate",
                    "Lorem",
                    "duis"
                ],
                "function": "Laboris dolore ad mollit sunt aliqua consectetur velit sint qui ullamco est.",
                "address": 30480705205
            },
            {
                "arguments": [
                    "proident",
                    "ipsum",
                    "labore"
                ],
                "function": "Sit magna adipisicing Lorem et dolor.",
                "address": 4948822819
            },
            {
                "arguments": [
                    "incididunt",
                    "laborum",
                    "minim",
                    "magna",
                    "exercitation"
                ],
                "function": "Fugiat do irure id laboris incididunt Lorem cupidatat sint.",
                "address": 26232535872
            },
            {
                "arguments": [
                    "commodo"
                ],
                "function": "Esse pariatur irure culpa id ipsum mollit dolor quis.",
                "address": 33431056507
            },
            {
                "arguments": [
                    "sunt",
                    "dolore"
                ],
                "function": "Lorem in esse est ipsum culpa deserunt.",
                "address": 25356277002
            },
            {
                "arguments": [
                    "quis",
                    "eu",
                    "nostrud",
                    "aute"
                ],
                "function": "Sint irure sunt aute irure cupidatat.",
                "address": 27269275024
            },
            {
                "arguments": [
                    "laborum",
                    "occaecat",
                    "esse",
                    "elit",
                    "ea"
                ],
                "function": "Sunt ex eu cillum excepteur duis esse id cillum nulla laboris minim irure.",
                "address": 7778327506
            },
            {
                "arguments": [
                    "voluptate",
                    "veniam",
                    "Lorem",
                    "culpa"
                ],
                "function": "Fugiat qui veniam elit culpa.",
                "address": 32978990563
            },
            {
                "arguments": [
                    "officia",
                    "aliquip",
                    "commodo"
                ],
                "function": "Aute sunt ea velit sunt eu ut.",
                "address": 20388675404
            }
        ],
        "friends": [
            {
                "id": 0,
                "name": "Traci Vasquez",
                "foos": null
            },
            {
                "id": 1,
                "name": "Glenn Michael",
                "foos": null
            },
            {
                "id": 2,
                "name": "Terrell Church",
                "foos": null
            }
        ],
        "greeting": "Hello, Dionne Maldonado! You have 4 unread messages.",
        "favoriteFruit": "apple"
    }
]


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        host = sys.argv[1]
        client = partycrasher.rest_client.RestClient(host)
    else:
        client = partycrasher.rest_client.RestClient()

    url = client.path_to('bullhooey', 'reports')
    for report in SAMPLE_REPORTS:
        requests.post(url, json=report)
