from mwclient import Site
import mwparserfromhell,re,time,os
from mwparserfromhell.nodes import *
from datetime import datetime
import mwparserfromhell as mw


def keep_top_10(dictionary):
    sorted_items = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    top_10 = dict(sorted_items[:10])
    new_dict = {}
    for key, value in top_10.items():
        new_dict[key] = value
    dictionary.clear()
    dictionary.update(new_dict)


def check_value_in_dict(dictionary, value):
    if value in dictionary.values():
        return True
    else:
        return False


class Polibot:
    def __init__(self,title,site):
        self.page = site.pages[title]
        self.code = mwparserfromhell.parse(self.page.text())
        self.out_poli_list = []
        self.poli_list = []
        self.huanhang_pattern = r'^[ \n]+$' #huanhang_pattern，检测是否由纯空格和换行符组成，布尔值
        self.out_separator_list=[",","，", ";", ":", ".","。", "!", "?", "-", "—","\"\"", "\'", "\'", "br"] #out_separator_list，被拒绝的间隔符列表，列表


    def contains_any(self, string, items):#被process_headings调用
        return any(item in string for item in items)


    def process_templates(self): #被perform_edit调用，查找信息框模板
        for template in self.code.filter_templates():
            if template.name.matches("AU信息框"):
                self.AU_process_infobox(infobox_template=template)
            if template.name.matches("人物信息框"):
                self.person_process_infobox(infobox_template=template)
            if template.name.matches("游戏信息框"):
                self.game_process_infobox(infobox_template=template)
            if template.name.matches("音乐信息框"):
                self.yinyue_process_infobox(infobox_template=template)
#----------------------------------infobox-----------------------------------------------#
    def AU_process_infobox(self,infobox_template): #被process_templates调用
        infobox_params = infobox_template.params
        for infobox_param in infobox_params:
            if infobox_param.name == "原名":
                self.process_param_yuanming(infobox_param)
            elif infobox_param.name == "常用译名":
                self.process_param_changyongyiming(infobox_param)
            elif infobox_param.name == "创始者":
                self.process_param_chuangshizhe(infobox_param)
            elif infobox_param.name == "现持有者":
                self.process_param_xianchiyouzhe(infobox_param)
            elif infobox_param.name == "参与制作者":
                self.process_param_canyuzhizuozhe(infobox_param)
            elif infobox_param.name == "主页":
                self.process_param_zhuye(infobox_param)
            elif infobox_param.name == "类型":
                self.process_param_type(infobox_param)
            elif infobox_param.name == "风格":
                self.process_param_fengge(infobox_param)
            elif infobox_param.name == "背景":
                self.process_param_beijing(infobox_param)
            elif infobox_param.name == "发布日期":
                self.process_param_faburiqi(infobox_param)


    def game_process_infobox(self,infobox_template): #被process_templates调用
        infobox_params = infobox_template.params
        for infobox_param in infobox_params:
            if infobox_param.name == "原名":
                self.process_param_yuanming(infobox_param)
            elif infobox_param.name == "常用译名":
                self.process_param_changyongyiming(infobox_param)
            elif infobox_param.name == "制作者":
                self.process_param_zhizuozhe(infobox_param)
            elif infobox_param.name == "引擎":
                self.process_param_yinqing(infobox_param)
            elif infobox_param.name == "主页":
                self.process_param_zhuye(infobox_param)
            elif infobox_param.name == "所属AU":
                self.process_param_suoshuAU(infobox_param)
            elif infobox_param.name == "发行时间":
                self.param_faxingshijian(infobox_param)


    def person_process_infobox(self,infobox_template): #被process_templates调用
        infobox_params = infobox_template.params
        for infobox_param in infobox_params:
            if infobox_param.name == "昵称":
                self.process_param_nicheng(infobox_param)
            elif infobox_param.name == "更新内容":
                self.process_param_gengxinneirong(infobox_param)
            elif infobox_param.name == "性别":
                self.process_param_xingbie(infobox_param)
            elif infobox_param.name == "活跃年份":
                self.process_param_huoyuenianfen(infobox_param)
            elif infobox_param.name == "生日":
                self.process_param_shengri(infobox_param)
            elif infobox_param.name == "代表作品":
                self.process_param_daibiaozuopin(infobox_param)
            elif infobox_param.name == "链接":
                self.process_param_lianjie(infobox_param)
            elif infobox_param.name == "外号":
                self.process_param_waihao(infobox_param)


    def yinyue_process_infobox(self,infobox_template): #被process_templates调用
        infobox_params = infobox_template.params
        for infobox_param in infobox_params:
            if infobox_param.name == "原名":
                self.process_param_yuanming(infobox_param)
            elif infobox_param.name == "常用译名":
                self.process_param_changyongyiming(infobox_param)
            elif infobox_param.name == "制作者":
                self.process_param_zhizuozhe(infobox_param)
            elif infobox_param.name == "音乐风格":
                self.process_param_yinyuefengge(infobox_param)
            elif infobox_param.name == "shichang":
                self.process_param_shichang(infobox_param)
            elif infobox_param.name == "BPM":
                self.process_param_BPM(infobox_param)
            elif infobox_param.name == "曲目格式":
                self.process_param_qumugeshi(infobox_param)
            elif infobox_param.name == "发行时间":
                self.param_faxingshijian(infobox_param)
            elif infobox_param.name == "所属AU":
                self.process_param_suoshuAU(infobox_param)
            elif infobox_param.name == "相关角色":
                self.process_param_xiangguanjuese(infobox_param)
#-------------------------------------game--------------------------------------------#
    def process_param_zhizuozhe(self, infobox_param): #被process_infobox调用
        param_templates = infobox_param.value.filter_templates()
        param_valie="制作者"
        have_parm_template = False
        have_set = False


        for param_template in param_templates:
            if param_template.name.matches("人物链接"):
                have_parm_template=True
                name_template = param_template
                name_params = name_template.params


                for name_param in name_params:
                    if name_param.name == "set":
                        have_set = True
                        if name_param.value == param_valie or re.match(self.huanhang_pattern,str(name_param.value)):
                            self.poli_list.append("“制作者”栏通过")
                        else:
                            self.out_poli_list.append("“制作者”栏的{{tl|人物链接}}模板的set参数没有填入正确的值")


        if not have_parm_template:self.out_poli_list.append("“制作者”栏未使用{{tl|人物链接}}模板")
        if not have_set and have_parm_template:self.out_poli_list.append("“制作者”栏的{{tl|人物链接}}模板没有set参数")


    def process_param_yinqing(self, infobox_param): #被process_infobox调用
        pass
    def process_param_suoshuAU(self, infobox_param): #被process_infobox调用
        pass
    def process_param_faxingshijian(self, infobox_param): #被process_infobox调用
        param_templates = infobox_param.value.filter_templates()
        have_parm_template = False
        have_set = False
        have_time_param=False


        for param_template in param_templates:
            if param_template.name.matches("日期"):
                have_parm_template=True
                time_template=param_template
                time_params=time_template.params
                for time_param in time_params:
                    if time_param.name == "1":
                        have_time_param=True
                        try:
                            datetime.strptime(str(time_param.value),'%Y-%m-%d')
                            self.poli_list.append("“发行时间”栏的{{tl|日期}}的匿名参数1参数通过")
                        except ValueError:
                            try:
                                datetime.strptime(str(time_param.value),'%Y-%m')
                                self.poli_list.append("“发行时间”栏的{{tl|日期}}的匿名参数1参数通过")
                            except ValueError:
                                try:
                                    datetime.strptime(str(time_param.value),'%Y')
                                    self.poli_list.append("“发行时间”栏的{{tl|日期}}的匿名参数1参数通过")
                                except ValueError:
                                    self.out_poli_list.append("“发行时间”栏的{{tl|日期}}模板填入了不被接受的参数")
                    elif time_param.name == "set":
                        have_set = True
                        if time_param.value == "发行时间":
                            self.poli_list.append("“发行时间”栏的{{tl|日期}}的set参数通过")
                        else:
                            self.out_poli_list.append("“发行时间”栏的{{日期}}模板的set参数没有填入正确的值")


        if not have_parm_template: self.out_poli_list.append("“发行时间”栏未使用{{tl|日期}}模板")
        if not have_set and have_parm_template:self.out_poli_list.append("“发行时间”栏的{{tl|日期}}模板没有set参数")
        if not have_time_param and have_parm_template: self.out_poli_list.append("{{tl|日期}}模板没有1（日期）参数")
#-------------------------------------yinyue--------------------------------------------#
    def process_param_yinyuefengge(self, infobox_param): #被process_infobox调用
        pass
    def process_param_shichang(self, infobox_param): #被process_infobox调用
        pass
    def process_param_BPM(self, infobox_param): #被process_infobox调用
        pass
    def process_param_qumugeshi(self, infobox_param): #被process_infobox调用
        pass
    def process_param_suoshuAU(self, infobox_param): #被process_infobox调用
        pass
    def process_param_xiangguanjuese(self, infobox_param): #被process_infobox调用
        pass
#-------------------------------------person--------------------------------------------#
    def process_param_nicheng(self, infobox_param): #被process_infobox调用
        pass
    def process_param_gengxinneirong(self, infobox_param): #被process_infobox调用
        pass
    def process_param_xingbie(self, infobox_param): #被process_infobox调用
        pass
    def process_param_huoyuenianfen(self, infobox_param): #被process_infobox调用
        pass
    def process_param_shengri(self, infobox_param): #被process_infobox调用
        pass
    def process_param_daibiaozuopin(self, infobox_param): #被process_infobox调用
        pass
    def process_param_lianjie(self, infobox_param): #被process_infobox调用
        pass
    def process_param_waihao(self, infobox_param): #被process_infobox调用
        pass
#-------------------------------------AU----------------------------------------------#
    def process_param_yuanming(self, infobox_param): #被process_infobox调用
        param_templates = infobox_param.value.filter_templates()
        param_valie="原名"
        have_parm_template = False
        have_set = False


        for param_template in param_templates:
            if param_template.name.matches("名称"):
                have_parm_template = True
                name_template = param_template
                name_params = name_template.params


                for name_param in name_params:
                    if name_param.name == "set":
                        have_set = True
                        if name_param.value == param_valie or re.match(self.huanhang_pattern,str(name_param.value)):
                            self.poli_list.append("“原名”栏通过")
                        else:
                            self.out_poli_list.append("“原名”栏的{{tl|名称}}模板的set参数没有填入正确的值")


        if not have_parm_template:self.out_poli_list.append("“原名”栏未使用{{tl|名称}}模板")
        if not have_set and have_parm_template:self.out_poli_list.append("“原名”栏的{{tl|名称}}模板没有set参数")


    def process_param_changyongyiming(self, infobox_param): #被process_infobox调用
        param_templates = infobox_param.value.filter_templates()
        param_valie="常用译名"
        have_parm_template = False
        have_set = False


        for param_template in param_templates:
            if param_template.name.matches("名称"):
                have_parm_template = True
                name_template = param_template
                name_params = name_template.params


                for name_param in name_params:
                    if name_param.name == "set":
                        have_set = True
                        if name_param.value == "正式译名" or name_param.value == "官方译名" or name_param.value == "民间译名" or re.match(self.huanhang_pattern,str(name_param.value)):
                            self.poli_list.append("“常用译名”栏通过")
                        else:
                            self.out_poli_list.append("“常用译名”栏的{{tl|名称}}模板的set参数没有填入正确的值")


        if not have_parm_template:self.out_poli_list.append("“常用译名”栏未使用{{tl|名称}}模板")
        if not have_set and have_parm_template:self.out_poli_list.append("“常用译名”栏的{{tl|名称}}模板没有set参数")


    def process_param_chuangshizhe(self, infobox_param): #被process_infobox调用
        param_templates = infobox_param.value.filter_templates()
        param_valie="创始者"
        have_parm_template = False
        have_set = False


        for param_template in param_templates:
            if param_template.name.matches("人物链接"):
                have_parm_template=True
                name_template = param_template
                name_params = name_template.params


                for name_param in name_params:
                    if name_param.name == "set":
                        have_set = True
                        if name_param.value == param_valie or re.match(self.huanhang_pattern,str(name_param.value)):
                            self.poli_list.append("“创始者”栏通过")
                        else:
                            self.out_poli_list.append("“创始者”栏的{{tl|人物链接}}模板的set参数没有填入正确的值")


        if not have_parm_template:self.out_poli_list.append("“创始者”栏未使用{{tl|人物链接}}模板")
        if not have_set and have_parm_template:self.out_poli_list.append("“创始者”栏的{{tl|人物链接}}模板没有set参数")


    def process_param_xianchiyouzhe(self, infobox_param): #被process_infobox调用
        param_templates = infobox_param.value.filter_templates()
        param_valie="现持有者"
        have_parm_template = False
        have_set = False


        for param_template in param_templates:
            if param_template.name.matches("人物链接"):
                have_parm_template = True
                name_template = param_template
                name_params = name_template.params


                for name_param in name_params:
                    if name_param.name == "set":
                        have_set = True
                        if name_param.value == param_valie or re.match(self.huanhang_pattern,str(name_param.value)):
                            self.poli_list.append("“现持有者”栏通过")
                        else:
                            self.out_poli_list.append("“现持有者”栏的{{tl|人物链接}}模板的set参数没有填入正确的值")


        if not have_parm_template:self.out_poli_list.append("“现持有者”栏未使用{{tl|人物链接}}模板")
        if not have_set and have_parm_template:self.out_poli_list.append("“现持有者”栏的{{tl|人物链接}}模板没有set参数")


    def process_param_canyuzhizuozhe(self, infobox_param): #被process_infobox调用
        param_templates = infobox_param.value.filter_templates()
        param_valie="参与制作者"
        have_parm_template = False
        have_set = False


        for param_template in param_templates:
            if param_template.name.matches("人物链接"):
                have_parm_template = True
                name_template = param_template
                name_params = name_template.params


                for name_param in name_params:
                    if name_param.name == "set":
                        have_set = True
                        if name_param.value == param_valie or re.match(self.huanhang_pattern,str(name_param.value)):
                            self.poli_list.append("“参与制作者”栏通过")
                        else:
                            self.out_poli_list.append("“参与制作者”栏的{{tl|人物链接}}模板的set参数没有填入正确的值")


        if not have_parm_template:self.out_poli_list.append("“参与制作者”栏未使用{{tl|人物链接}}模板")
        if not have_set and have_parm_template:self.out_poli_list.append("“参与制作者”栏的{{tl|人物链接}}模板没有set参数")


    def process_param_zhuye(self, infobox_param): #被process_infobox调用
        param_templates = infobox_param.value.filter_templates()
        have_parm_template = False


        for param_template in param_templates:
            if param_template.name.matches("主页"):
                have_parm_template = True
                url_regex = re.compile(r'^https?://\S+$')
                url=str(param_template.get(2))
                if url_regex.match(url):
                    self.poli_list.append("“主页”栏通过")
                else:
                    self.out_poli_list.append("{{tl|主页}}模板参数错误")
                have_parm_template=True


        if not have_parm_template and have_parm_template:self.out_poli_list.append("“主页”栏未使用{{tl|主页}}模板")


    def process_param_type(self, infobox_param): #被process_infobox调用
        AU_type_list=["平行时间轴","准则变化","正典偏离","续写历史","扩展宇宙","世界观变动","宇宙迁移","角色错位","元素代入","元素混杂","跨界交叉","未知","其他",",","br"," ","\n"]
        if any(x in str(infobox_param.value) for x in AU_type_list):
            self.poli_list.append("“类型”栏通过")
        else:
            self.out_poli_list.append("“类型”栏填入了不规范的类型")


    def process_param_fengge(self, infobox_param): #被process_infobox调用
        if any(x in str(infobox_param.value) for x in self.out_separator_list):
            self.out_poli_list.append("“风格”栏填填入多个但使用了除、以外的符号进行间隔")
        else:
            self.poli_list.append("“风格”栏通过")


    def process_param_beijing(self, infobox_param): #被process_infobox调用
        if any(x in str(infobox_param.value) for x in self.out_separator_list):
            self.out_poli_list.append("“背景”栏填填入多个但使用了除、以外的符号进行间隔")
        else:
            self.poli_list.append("“背景”栏通过")


    def process_param_faburiqi(self, infobox_param): #被process_infobox调用
        param_templates = infobox_param.value.filter_templates()
        param_valie="发布日期"
        have_parm_template = False
        have_set = False
        have_time_param=False


        for param_template in param_templates:
            if param_template.name.matches("日期"):
                have_parm_template=True
                time_template=param_template
                time_params=time_template.params
                for time_param in time_params:
                    if time_param.name == "1":
                        have_time_param=True
                        try:
                            datetime.strptime(str(time_param.value),'%Y-%m-%d')
                            self.poli_list.append("“发布日期”栏的{{tl|日期}}的匿名参数1参数通过")
                        except ValueError:
                            try:
                                datetime.strptime(str(time_param.value),'%Y-%m')
                                self.poli_list.append("“发布日期”栏的{{tl|日期}}的匿名参数1参数通过")
                            except ValueError:
                                try:
                                    datetime.strptime(str(time_param.value),'%Y')
                                    self.poli_list.append("“发布日期”栏的{{tl|日期}}的匿名参数1参数通过")
                                except ValueError:
                                    self.out_poli_list.append("“发布日期”栏的{{tl|日期}}模板填入了不被接受的参数")
                    elif time_param.name == "set":
                        have_set = True
                        if time_param.value == "发布日期":
                            self.poli_list.append("“发布日期”栏的{{tl|日期}}的set参数通过")
                        else:
                            self.out_poli_list.append("“发布日期”栏的{{日期}}模板的set参数没有填入正确的值")


        if not have_parm_template: self.out_poli_list.append("“发布日期”栏未使用{{tl|日期}}模板")
        if not have_set and have_parm_template:self.out_poli_list.append("“发布日期”栏的{{tl|日期}}模板没有set参数")
        if not have_time_param and have_parm_template: self.out_poli_list.append("{{tl|日期}}模板没有1（日期）参数")


#-------------------------------------other----------------------------------------------#



    def process_headings(self, headings): #被process_code调用，检查标题
        if headings != []:
            norm_headings = ["简介","列表","背景故事","世界观","集","信息","琐事","历程","发展","画廊","经历","作品","曲源","内容","其他","其它","剧情"]
            previous_level = 1
            is_out_process_headings = False
            is_across_headings = False


            for heading in headings:
                level = heading.level


                if level - previous_level > 1:
                    is_across_headings=True


                previous_level = level


                if level == 2 and not self.contains_any(str(heading.title.strip()), norm_headings):
                    is_out_process_headings=True


            if is_across_headings:self.out_poli_list.append("页面中使用了跨层级的章节标题")
            if is_out_process_headings:self.out_poli_list.append("使用了除规范化栏目所述标题以外的标题")
        else:
            self.out_poli_list.append("全页没有章节标题")


    def check_chinese_ratio(self): #被process_code调用，检查中文比例
        re_han = re.compile(r"[\u4e00-\u9fa5]")
        total = len(re.findall(r'\w+', str(self.code)))
        han_cnt = len(re_han.findall(str(self.code)))
        ratio = round(han_cnt / total, 2)


        if ratio < 0.1:
            self.out_poli_list.append("全文或大部分内容不是由现代汉语组成")


    def process_code(self): #被perform_edit调用，检查全页代码
        templates = self.code.filter_templates()
        headings = self.code.filter_headings()


        if headings:
            self.process_headings(headings)
        else:
            self.out_poli_list.append("全页没有章节标题")


        self.check_chinese_ratio()


    def generate_op_string(self): #被perform_edit调用，检查中文比例
        new_out_poli_list=[]
        for i in self.out_poli_list:
            if i not in new_out_poli_list:
                new_out_poli_list.append(i)
        self.out_poli_list = new_out_poli_list
        return ','.join(self.out_poli_list)


    def perform_edit(self): #主方法，执行编辑
        self.process_templates()
        self.process_code()
        templates = self.code.filter_templates()
        op_a = False
        op_b = False


        if self.out_poli_list:
            if templates[0].name.matches("请求修改"):
                templates[0].add(2, self.generate_op_string())
            else:
                zuijin = mw.nodes.Template(name="请求修改")
                zuijin.add(1, "adof")
                zuijin.add(2, self.generate_op_string())
                self.code.insert(0, zuijin)
            op_a = True
        else:
            for template in templates:
                if template.name.matches("请求修改"):
                    self.code.remove(template)
                    op_b = True


        print("检查点")
        if op_a or op_b:
            self.page.edit(str(self.code), summary="Polibot beta0.2D 作出的编辑")


        print(self.out_poli_list, self.poli_list)
#---------------------------------main-----------------------------------------#


current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'password.txt')
f = open(file_path,'r',encoding = 'utf-8')


ua="UTCWIKI Polibot"
site = Site('utcwiki.com', path='/', clients_useragent=ua)
site.login('polibot', str(f.read()))
f.close()
all_count=0 #all_count，整个循环的运行次数，整数
not_title=0 #not_title，没有最终结果的次数，整数
recent_change_old_dict = {}
while True:
    recent_changes = site.recentchanges(namespace=0)


    desired_count = 10 #desired_count，总共要获取的最近更改条数，整数
    count = 0 #count，当前获取到的条数，整数


    huanhang_pattern = r'^[ \n]+$' #huanhang_pattern，检测是否由纯空格和换行符组成，布尔值


    recent_change_dict={}
    recent_change_simplify_dict={}
    is_recent_change_simplify_dict=False


    for index,change in enumerate(recent_changes):#获取最近更改
        timestamp = time.mktime(change['timestamp'])
        title = change['title']
        if title not in recent_change_dict:
            inspect_title = title
            inspect_page = site.pages[inspect_title]
            exists = inspect_page.exists
            inspect_categories = inspect_page.categories()
            is_disambiguation_or_undertale = False


            for category in inspect_categories:
                if str(category.name) == '分类:消歧义页' or str(category.name) == '分类:Undertale相关':
                    is_disambiguation_or_undertale = True
            if exists and not inspect_page.redirect and not is_disambiguation_or_undertale:
                recent_change_dict[title] = timestamp
            else:
                print("排除已删除,重定向,消歧义,Undertale相关的页面")
        count += 1
        if count >= desired_count:
            break


    title_list=[]


    if all_count!=0:#获取去重后的最近更改
        for key, value in recent_change_dict.items():
            if not check_value_in_dict(recent_change_old_dict,value):
                recent_change_simplify_dict[key] = value
        is_recent_change_simplify_dict = True #recent_change_dict2_b，是否选择去重结果，布尔值


    if is_recent_change_simplify_dict:
        for key in recent_change_simplify_dict.keys():
            title_list.append(key)
        print("至少已经有过一次循环，获取去重后的结果")
    else:
        for key in recent_change_dict.keys():
            title_list.append(key)
        print("第一次循环")


    print(title_list)


    if title_list!=[]:
        not_title = 0
        for title in title_list:
            polibot = Polibot(site=site,title=title)
            polibot.perform_edit()
    else:
        print("无更新")
        not_title+=1


    all_count+=1
    for key, value in recent_change_dict.items():
        recent_change_old_dict[key] = value


    keep_top_10(recent_change_old_dict)
    print("recent_change_dict:",recent_change_dict)
    print("recent_change_simplify_dict:",recent_change_simplify_dict)
    print("recent_change_old_dict:",recent_change_old_dict)
    print("is_recent_change_simplify_dict:",is_recent_change_simplify_dict)
    print("not_title:",not_title)


    if not_title >= 20:
        print("3000秒冷却")
        time.sleep(3000)
    elif not_title >= 10:
        print("300秒冷却")
        time.sleep(300)
    else:
        print("30秒冷却")
        time.sleep(30)