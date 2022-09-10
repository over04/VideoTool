class Parse_Func:
    def __init__(self, rule: dict):
        '''
        rule example:
        [
            {
                name:str, #命令的字符
                aliases:tuple or list, #其他可以唤醒命令的字符,
                require:True or False #是否为必须
                detail: #详细介绍
                type: #数据类型 int or string or float
                defeat: 默认的数据

            }
        ]
        :param rule:
        '''
        self.__rule = []
        rule['require'] = True
        add_return = self.add_rule(rule)
        if add_return is False:
            raise ValueError('')

    def pare_string(self, string: str):
        funcs = {_[0]: _[1].strip() for _ in [i.split('=') for i in string.split('-') if '=' in i]}  # -name=360 -cid=1
        dic = {}
        for each_rule in self.__rule:
            func = each_rule['type']
            # and (each_rule['name'] not in funcs or all(map(lambda x:x not in funcs,each_rule['aliases']))):
            name = each_rule['name']
            if name in funcs:
                dic[name] = func(funcs[name])
            else:  # any(map(lambda x: x in funcs, each_rule['aliases'])):
                for i in each_rule['aliases']:
                    if i in funcs:
                        dic[name] = func(funcs[i])
                        break
                else:
                    if each_rule['require'] is True:
                        return self.get_help()
                    else:
                        dic[name] = each_rule['defeat']
        return dic

    def get_help(self):
        help_string = ''
        for each_rule in self.__rule:
            name = each_rule.get('name')
            aliases = list(each_rule.get('aliases'))
            detail = each_rule.get('detail')
            help_string += f"{name} or {aliases} : {each_rule.get('type')}({name}) {detail}\n"
        return help_string

    def add_rule(self, rule: dict):
        if 'name' not in rule or 'defeat' not in rule:
            return False
        rule['aliases'] = rule.get('aliases', [])
        rule['require'] = rule.get('require', False)
        rule['type'] = rule.get('type', str)
        if not isinstance(rule['defeat'], rule['type']):
            return False
        rule['detail'] = rule.get('detail', '')
        self.__rule.append(rule)
        return True


if __name__ == '__main__':
    parse = Parse_Func(
        {
            'name': 'search_source',
            'aliases': ('s',),
            'defeat': '360',
            'type': str
        }
    )
    parse.add_rule(
        {
            'name': 'count',
            'aliases': ('c',),
            'defeat': 1,
            'type': int
        }
    )
    parse.add_rule(
        {
            'name': 'name',
            'aliases': ('n',),
            'defeat': '夏日重现',
            'type': str
        }
    )
    parse.add_rule(
        {
            'name': 'page',
            'aliases': ('p',),
            'defeat': 1,
            'type': int
        }
    )
    parse.add_rule(
        {
            'name': 'pagesize',
            'aliases': ('size',),
            'defeat': 30,
            'type': int
        }
    )
    print(parse.pare_string('-s=pixivic -c=5 -name=原神'))
