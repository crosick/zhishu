#-*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, QuestionForm,\
    AnswerForm
from .. import db
from ..models import Permission, Role, User, Question, Answer, Tag, Vote, Unvote
from ..decorators import admin_required, permission_required

@main.after_app_request
def after_request(response):
    """在视图函数处理完后统一调用，负责记录下响应过慢的 query """    
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    """为了在测试完后关掉服务器"""
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/', methods=['GET', 'POST'])
def index():
    """首页的。。。没必要注释吧"""
    page = request.args.get('page', 1, type=int)
    tags = Tag.query.all()
    tag = request.args.get('tag')
    show_followed = False
    if current_user.is_authenticated():
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_questions
    elif tag:
        query = Question.query.filter(Question.tags.any(tag=tag))

    else:
        query = Question.query
    pagination = query.order_by(Question.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    questions = pagination.items
    return render_template('index.html',  questions=questions, tags=tags,
                           show_followed=show_followed, pagination=pagination)

@main.route('/delete/<int:id>')
@login_required
def delete_question(id):
    """删除一个问题"""
    question = Question.query.get_or_404(id)
    if current_user != question.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('.index'))



@main.route('/search', methods=['GET'])
def search_results():
    """搜索问题"""
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('query')
    query = Question.query.whoosh_search(keyword)

    pagination = query.order_by(Question.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    questions = pagination.items
    return render_template('search_results.html', query=keyword, 
                            questions=questions, pagination=pagination)

@main.route('/ask',methods=['GET', 'POST'])
@login_required
def ask():
    """发布问题"""
    form = QuestionForm()     
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():

        question = Question(title=form.title.data,
                            body=form.body.data,
                            author=current_user._get_current_object())        
        

        tag_list = form.tags.data.split(',')
        for tag_item in tag_list:
            tag = Tag.query.filter_by(tag=tag_item).first()
            if not tag:
                tag = Tag(tag=tag_item)
            question.tags.append(tag)

        db.session.add(tag)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('.index'))
    return render_template('ask.html', form=form)


@main.route('/user/<username>')
def user(username):
    """用户个人主页"""
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.questions.order_by(Question.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    questions = pagination.items
    return render_template('user.html', user=user, questions=questions,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """编辑个人信息"""
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    """admin编辑个人信息"""
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    """问题页面"""
    question = Question.query.get_or_404(id)
    question.visited_once()
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(body=form.body.data,
                          question=question,
                          author=current_user._get_current_object())
        db.session.add(answer)
        flash('Your answer has been published.')
        return redirect(url_for('.question', id=question.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (question.answers.count() - 1) / \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1

    pagination = question.answers.order_by(Answer.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    answers = pagination.items
    return render_template('question.html', question=question, form=form,
                           answers=answers, pagination=pagination)


@main.route('/vote/<int:answer_id>')
@login_required
def vote(answer_id):
    """给回答投赞成票"""
    answer = Answer.query.get(answer_id)
    user = current_user
    votes = Vote.query.filter_by(user=user, answer=answer)
    if votes.count() == 0:
        vote = Vote(user=user, answer=answer)
        db.session.add(vote)
    else:
        db.session.delete(votes[0])
    db.session.commit()
    return redirect(request.args.get('next'))


@main.route('/unvote/<int:answer_id>')
@login_required
def unvote(answer_id):
    """给回答投反对票"""
    answer = Answer.query.get(answer_id)
    user = current_user
    unvotes = Unvote.query.filter_by(user=user, answer=answer)
    if unvotes.count() == 0:
        unvote = Unvote(user=user, answer=answer)
        db.session.add(unvote)
    else:
        db.session.delete(unvotes[0])
    db.session.commit()
    return redirect(request.args.get('next'))


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    """编辑问题"""
    question = Question.query.get_or_404(id)
    if current_user != question.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = QuestionForm()
    if form.validate_on_submit():
        question.title = form.title.data
        question.body = form.body.data
        # db.session.add(question)
        flash('The question has been updated.')
        return redirect(url_for('.question', id=question.id))
    form.title.data = question.title
    form.body.data = question.body
    form.tags.data = ','.join([tag.tag for tag in question.tags])
    return render_template('edit_question.html', form=form, question=question)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    """关注一个人"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    """取关一个人"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/all')
@login_required
def show_all():
    """显示全部问题"""
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    """显示关注的人的问题"""
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Answer.query.order_by(Answer.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    answers = pagination.items
    return render_template('moderate.html', answers=answers,
                           pagination=pagination, page=page)


@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    answer = Answer.query.get_or_404(id)
    answer.disabled = False
    db.session.add(answer)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))


@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    answer = Answer.query.get_or_404(id)
    answer.disabled = True
    db.session.add(answer)
    return redirect(url_for('.moderate',
                            page=request.args.get('page', 1, type=int)))
