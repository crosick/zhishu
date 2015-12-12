#-*- coding:utf-8 -*-
import sadisplay
from app import models

desc = sadisplay.describe([models.User,models.Question,models.Answer,models.Role,models.Tag,models.Follow,models.Vote, models.Unvote,models.assoc_question_tag_table])
file = open('schema.dot', 'w')
file.write(sadisplay.dot(desc).encode('utf-8'))
file.close()