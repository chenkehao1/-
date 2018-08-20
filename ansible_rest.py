#!/usr/bin/env python
#-*- coding: utf-8 -*-
import ansible.runner
import ansible.inventory
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')


def ansible_HD(a):
    hosts = ansible.inventory.Inventory()
    ans = ansible.runner.Runner(module_name='shell', module_args=a, timeout=5, inventory=hosts, subset='all')
    data = ans.run()
    return data#json.dumps(o, sort_keys=True, separators=(',', ': '))


def fenxi_free():
    data = ansible_HD('free')
    print 'CentOS'+'============='+'total'+'========='+'used'+'=========='+'free'+'========'+'Take up'
    for cont in data['contacted']:
        sys_vl = data["contacted"][cont]["stdout"].split(' ')
        i_list = []
        for i in sys_vl:
            if i == '':continue
            i_list.append(i)
        baifenbi = "%.2f%%" % (eval(i_list[7] + '/' + i_list[6] + '.' + '*100'))
        i_list.append(baifenbi)
        print '-%s------%s------%s------%s------%s' % (cont, i_list[6], i_list[7], i_list[8], i_list[15])


def fenxi_df(dig):
    data = ansible_HD('df -h')
    for cont1 in data['contacted']:
        df = re.compile('(\d.?)%').findall(data['contacted'][cont1]['stdout'])
        for i in df:
            if int(i) >= int(dig):
                print cont1
                print data['contacted'][cont1]['stdout']

def main():
    dig = sys.argv[2]
    cmd = sys.argv[1]
    if cmd == 'free':
        fenxi_free()
    elif cmd == 'df':
        fenxi_df(dig)
    else:
        fenxi_free()
        print '<======================================================================================================>'
        fenxi_df(dig)


if __name__ == '__main__':
    main()
