# -*- coding: utf-8 -*-
from front_handlers import IndexHandler,SignInHandler,FrontRegistHandler,ForgetPwdHandler, SignupHandler,testHandler,\
 frontBulletinsHandler, bulletinDetailHandler, courseDevelopHandler, courseIntroHandler, courseTeachersHandler, fileDownLoadPageHandle, fileDownLoadInfoHandler,\
getSortLimitFileHandler, communityHandler, addArticleHandler, articleDetailHandler,getSortLimitArticlesHandler, ResetPwdHandler,\
profileHandler

frontUrls = [
    (r"^/$",IndexHandler),
    (r"^/signin",SignInHandler),
    (r"^/regist",FrontRegistHandler),
    (r"^/forgetpwd",ForgetPwdHandler),
    (r"^/logout",SignupHandler),
    (r"^/test",testHandler),
    (r"^/course_develop$",courseDevelopHandler),
    (r"^/course_teachers$",courseTeachersHandler),
    (r"^/course_intro$",courseIntroHandler),
    (r"^/bulletin$",frontBulletinsHandler),
    (r"^/bulletin_detail",bulletinDetailHandler),
    (r"^/resource",fileDownLoadPageHandle),
    (r"^/resource_info$",fileDownLoadInfoHandler),
    (r"^/get_file",getSortLimitFileHandler),
    (r"^/community",communityHandler),
    (r"^/add_article/",addArticleHandler),
    (r"^/article_detail",articleDetailHandler),
    (r"^/get_articles",getSortLimitArticlesHandler),
    (r"^/reset_pwd",ResetPwdHandler),
    (r"^/profile",profileHandler),
]