from mwclient import Site
import mwparserfromhell,re,time,os
from mwparserfromhell.nodes import *
from datetime import datetime
import mwparserfromhell as mw

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'password.txt')
f = open(file_path,'r',encoding = 'utf-8')

ua="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.3202.9 Safari/5336"
site = Site('utcwiki.com', path='/', clients_useragent=ua)
site.login('polibot', str(f.read()))
f.close()
all_count=0 #all_count，整个循环的运行次数，整数
while True:
    recent_changes = site.recentchanges(namespace=0)

    desired_count = 10 #desired_count，总共要获取的最近更改条数，整数
    count = 0 #count，当前获取到的条数，整数

    huanhang_pattern = r'^[ \n]+$' #huanhang_pattern，检测是否由纯空格和换行符组成，布尔值

    recent_change_dict={}
    recent_change_dict2={}
    recent_change_dict2_b=False

    for index,change in enumerate(recent_changes):
        timestamp1 = time.mktime(change['timestamp'])
        if index==0:
            frist_timestamp=timestamp1 #frist_timestamp，最新一次更改的时间戳，整数
        recent_change_dict[change['title']] = timestamp1
        count += 1
        if count >= desired_count:
            break

    title_list=[]
    print(frist_timestamp)
    if frist_timestamp and all_count!=0:
        for key, value in recent_change_dict.items():
            if int(value) > int(frist_timestamp):
                recent_change_dict2[change['title']] = timestamp1
        recent_change_dict2_b=True #recent_change_dict2_b，是否选择去重结果，布尔值

    if recent_change_dict2_b:
        for key in recent_change_dict2.keys():
            title_list.append(key)
        print("至少已经有过一次循环，获取去重后的结果")
    else:
        for key in recent_change_dict.keys():
            title_list.append(key)
        print("第一次循环")
    print(title_list)
    if title_list!=[]:
        for title in title_list:
            page = site.pages[title]
            code = mwparserfromhell.parse(page.text())

            has_AUc = False
            has_AUi = False

            for template in code.filter_templates():
                if template.name.matches('AU条目'):
                    has_AUc = True
                elif template.name.matches('AU信息框'):
                    has_AUi = True

            if has_AUc or has_AUi:

                out_poli_list=[]
                poli_list=[]
                templates = code.filter_templates()
                headings = code.filter_headings()
                type_template=False

                out_norm_headings=False
                parm_template_faburiqi=False
                parm_template_yuanming=False
                parm_template_xianchiyouzhe=False
                parm_template_changyongyiming=False
                parm_template_zhuye=False
                parm_template_canyuzhizuozhe=False
                parm_template_chuangshizhe=False
                parm_template_faburiqi=False
                set_yuanming=False
                set_zhengshiyiming=False
                set_chuangshizhe=False
                set_xianchiyouzhe=False
                set_canyuzhizuozhe=False
                set_xianchiyouzhe=False
                set_canyuzhizuozhe=False
                set_faburiqi=False
                op_a=False
                op_b=False
                print("检查点")
                for template in templates:
                    if template.name.matches("AU信息框"):
                        type_template=True
                        infobox_template=template
                        infobox_params=infobox_template.params
                        for infobox_param in infobox_params:
                            if infobox_param.name == "原名":
                                param_templates=infobox_param.value.filter_templates()
                                for param_template in param_templates:
                                    if param_template.name.matches("名称"):
                                        name_template=param_template
                                        name_params=name_template.params
                                        for name_param in name_params:
                                            if name_param.name == "set":
                                                set_yuanming=1
                                                if name_param.value == "原名":
                                                    poli_list.append("“原名”栏通过")
                                                else:
                                                    out_poli_list.append("“原名”栏的{{名称}}模板的set参数没有填入正确的值")
                                        if not set_yuanming:
                                            out_poli_list.append("“原名”栏的{{tl|名称}}模板没有set参数")
                                        parm_template_yuanming=1
                                ine=re.findall(r'[^ \n]',str(infobox_param.value)) 
                                if not parm_template_yuanming and ine != []: out_poli_list.append("“原名”栏未使用{{tl|名称}}模板")
                            elif infobox_param.name == "常用译名":
                                param_templates=infobox_param.value.filter_templates()
                                for param_template in param_templates:
                                    if param_template.name.matches("名称"):
                                        name_template=param_template
                                        name_params=name_template.params
                                        for name_param in name_params:
                                            if name_param.name == "set":
                                                set_zhengshiyiming=1
                                                if name_param.value == "正式译名" or name_param.value == "官方译名" or name_param.value == "民间译名" or re.match(huanhang_pattern,str(name_param.value)):
                                                    poli_list.append("“常用译名”栏通过")
                                                else:
                                                    out_poli_list.append("“常用译名”栏的{{tl|名称}}模板的set参数没有填入正确的值")
                                        if not set_zhengshiyiming:
                                            out_poli_list.append("“常用译名”栏的{{tl|名称}}模板没有set参数")
                                        parm_template_changyongyiming=1
                                if not parm_template_changyongyiming: out_poli_list.append("“常用译名”栏未使用{{tl|名称}}模板")
                            elif infobox_param.name == "创始者":
                                param_templates=infobox_param.value.filter_templates()
                                for param_template in param_templates:
                                    if param_template.name.matches("人物链接"):
                                        name_template=param_template
                                        name_params=name_template.params
                                        for name_param in name_params:
                                            if name_param.name == "set":
                                                set_chuangshizhe=1
                                                if name_param.value == "创始者" or re.match(huanhang_pattern,str(name_param.value)):
                                                    poli_list.append("“创始者”栏通过")
                                                else:
                                                    out_poli_list.append("“创始者”栏的{{tl|人物链接}}模板的set参数没有填入正确的值")
                                        if not set_chuangshizhe:
                                            out_poli_list.append("“创始者”栏的{{tl|人物链接}}模板没有set参数")
                                        parm_template_chuangshizhe=1
                                if not parm_template_chuangshizhe: out_poli_list.append("“创始者”栏未使用{{tl|人物链接}}模板")
                            elif infobox_param.name == "现持有者":
                                param_templates=infobox_param.value.filter_templates()
                                for param_template in param_templates:
                                    if param_template.name.matches("人物链接"):
                                        name_template=param_template
                                        name_params=name_template.params
                                        for name_param in name_params:
                                            if name_param.name == "set":
                                                set_xianchiyouzhe=1
                                                if name_param.value == "现持有者" or re.match(huanhang_pattern,str(name_param.value)):
                                                    poli_list.append("“现持有者”栏通过")
                                                else:
                                                    out_poli_list.append("“现持有者”栏的{{名称}}模板的set参数没有填入正确的值")
                                        if not set_xianchiyouzhe:
                                            out_poli_list.append("“现持有者”栏的{{tl|人物链接}}模板没有set参数")
                                        parm_template_xianchiyouzhe=1
                                if not parm_template_xianchiyouzhe: out_poli_list.append("“现持有者”栏未使用{{tl|人物链接}}模板")
                            elif infobox_param.name == "参与制作者":
                                param_templates=infobox_param.value.filter_templates()
                                for param_template in param_templates:
                                    if param_template.name.matches("人物链接"):
                                        name_template=param_template
                                        name_params=name_template.params
                                        for name_param in name_params:
                                            if name_param.name == "set":
                                                set_canyuzhizuozhe=1
                                                if name_param.value == "参与制作者" or re.match(huanhang_pattern,str(name_param.value)):
                                                    poli_list.append("“参与制作者”栏通过")
                                                else:
                                                    out_poli_list.append("“参与制作者”栏的{{tl|人物链接}}模板的set参数没有填入正确的值")
                                        if not set_canyuzhizuozhe:
                                            out_poli_list.append("“参与制作者”栏的{{tl|人物链接}}模板没有set参数")
                                        parm_template_canyuzhizuozhe=1
                                if not parm_template_canyuzhizuozhe: out_poli_list.append("“参与制作者”栏未使用{{tl|人物链接}}模板")
                            elif infobox_param.name == "主页":
                                param_templates=infobox_param.value.filter_templates()
                                for param_template in param_templates:
                                    if param_template.name.matches("主页"):
                                        url_regex = re.compile(r'^https?://\S+$')
                                        url=str(param_template.get(2))
                                        if url_regex.match(url):
                                            poli_list.append("“主页”栏通过")
                                        else:
                                            out_poli_list.append("{{tl|主页}}模板参数错误")
                                        parm_template_zhuye=1
                                if not parm_template_zhuye: out_poli_list.append("“主页”栏未使用{{tl|主页}}模板")
                            elif infobox_param.name == "类型":
                                AU_type_list=["平行时间轴","准则变化","正典偏离","续写历史","扩展宇宙","世界观变动","宇宙迁移","角色错位","元素代入","元素混杂","跨界交叉","未知","其他"," ","\n"]
                                if any(element in str(infobox_param.value) for element in AU_type_list):
                                    poli_list.append("“类型”栏通过")
                                else:
                                    out_poli_list.append("“类型”栏填入了不规范的类型")
                            elif infobox_param.name == "风格":
                                out_separator_list=[",","，", ";", ":", ".","。", "!", "?", "-", "—","\"\"", "\'", "\'"]
                                if any(element in str(infobox_param.value) for element in out_separator_list):
                                    out_poli_list.append("“风格”栏填填入多个但使用了除、以外的符号进行间隔")
                                else:
                                    poli_list.append("“风格”栏通过")
                            elif infobox_param.name == "背景":
                                if any(element in str(infobox_param.value) for element in out_separator_list):
                                    out_poli_list.append("“背景”栏填填入多个但使用了除、以外的符号进行间隔")
                                else:
                                    poli_list.append("“背景”栏通过")
                            elif infobox_param.name == "发布日期":
                                param_templates=infobox_param.value.filter_templates()
                                for param_template in param_templates:
                                    if param_template.name.matches("日期"):
                                        time_template=param_template
                                        time_params=time_template.params
                                        for time_param in time_params:
                                            if time_param.name == "1":
                                                format_str = '%Y-%m-%d'
                                                try:
                                                    datetime.strptime(str(time_param.value),format_str)
                                                    poli_list.append("“发布日期”栏的{{tl|日期}}的匿名参数1参数通过")
                                                except ValueError:
                                                    out_poli_list.append("“发布日期”栏的{{tl|日期}}模板填入了不被接受的参数")
                                            elif time_param.name == "set":
                                                set_faburiqi=1
                                                if time_param.value == "发布日期":
                                                    poli_list.append("“发布日期”栏的{{tl|日期}}的set参数通过")
                                                else:
                                                    out_poli_list.append("“发布日期”栏的{{日期}}模板的set参数没有填入正确的值")
                                        if not set_faburiqi:
                                            out_poli_list.append("“发布日期”栏的{{tl|日期}}模板没有set参数")
                                        parm_template_faburiqi=1
                                if not parm_template_faburiqi: out_poli_list.append("“发布日期”栏未使用{{tl|日期}}模板")
                if headings != []:
                    norm_headings=["简介","代入列表","错位列表","背景故事","世界观","漫画集","音乐集","集","角色信息","琐事","历程","画廊","经历","作品","曲源","内容"]
                    previous_level = 1
                    for heading in headings:
                        level = heading.level
                        if level - previous_level > 1:
                            out_poli_list.append("页面中使用了跨层级的章节标题")
                            continue
                        previous_level = level
                        if level == 2 and str(heading.title.strip()) not in norm_headings:
                            out_norm_headings=True
                    if out_norm_headings:
                        out_poli_list.append("使用了除规范化栏目所述标题以外的标题")
                else:
                    out_poli_list.append("全页没有章节标题")

                re_han = re.compile(r"[\u4e00-\u9fa5]")

                def check_chinese_ratio(code):
                    total = len(re.findall(r'\w+', code))
                    han_cnt = len(re_han.findall(code))
                    ratio = round(han_cnt / total, 2)
                    if ratio >= 0.5:
                        return True
                    else:
                        return False

                is_high_ratio = check_chinese_ratio(str(code))
                if is_high_ratio:
                    pass
                else:
                    out_poli_list.append("全文或大部分内容由非现代汉语组成")

                op=""#op,触发的页面处理政策，字符串
                for item in out_poli_list:
                    op=op+","+item

                if op!="":
                    if code.filter_templates()[0].name.matches("请求修改"):
                        code.filter_templates()[0].add(2,op)
                    else:
                        zuijin = mw.nodes.Template(name="请求修改") #zuijin，要插入的请求修改模板，字符串
                        zuijin.add(1,"adof")
                        zuijin.add(2,op)
                        code.insert(0,zuijin)
                    op_a=True
                else:
                    for template in templates:
                        if template.name.matches("请求修改"):
                            code.remove(template)
                            op_b=True

                print("检查点2")

                if op_a or op_b:
                    page.edit(str(code),summary="Polibot beta0.1C 作出的编辑")
                    
                    print(out_poli_list,poli_list,op)
            else:
                print("不是AU条目")
    else:
        print("无更新")
    all_count+=1
    time.sleep(30)