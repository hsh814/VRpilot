import difflib
#from main.utils.code_util import format_c_code

def diff_2_seq(s1, s2):
    """
    http://pymotw.com/2/difflib/
    """

    diff = []

    matcher = difflib.SequenceMatcher(None, s1, s2)
    for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):

        if tag == 'delete':
            # print('Delete %s from positions [%d:%d]\n' % (s1[i1:i2], i1, i2))
            diff.append({'Delete': (s1[i1:i2], i1, i2)})
            del s1[i1:i2]

        elif tag == 'equal':
            # print('The sections [%d:%d] of s1 and [%d:%d] of s2 are the same\n' % \
            #     (i1, i2, j1, j2))
            diff.append({'Equal': ((i1, i2, j1, j2))})

        elif tag == 'insert':
            # print('Insert %s from [%d:%d] of s2 into s1 at %d\n' % \
            #     (s2[j1:j2], j1, j2, i1))
            diff.append({'Insert': (s2[j1:j2], j1, j2, i1)})
            s1[i1:i2] = s2[j1:j2]

        elif tag == 'replace':
            # print('Replace %s from [%d:%d] of s1 with %s from [%d:%d] of s2\n' % (
            # s1[i1:i2], i1, i2, s2[j1:j2], j1, j2))
            diff.append({'Replace': (s1[i1:i2], i1, i2, s2[j1:j2], j1, j2)})
            s1[i1:i2] = s2[j1:j2]

    diff = reversed(diff)

    return diff


def print_diff(s1, s2):

    changed_line_cnt=0

    # s1 = format_c_code(c1).split("\n")
    # s2 = format_c_code(c2).split("\n")

    diff = diff_2_seq(s1, s2)

    print("Code changes:\n")

    diff_str = ''

    for d in diff:

        edit_type = list(d.keys())[0]

        if edit_type == 'Delete':
            if '\n'.join(d[edit_type][0]).strip() != '':
                print('Delete:\n%s from Line[%d:%d]\n' % (
                '\n'.join(d[edit_type][0]), d[edit_type][1], d[edit_type][2]))
                diff_str += ('Delete:\n%s\n' % ('\n'.join(d[edit_type][0])))
                changed_line_cnt += len(d[edit_type][0])

        elif edit_type == 'Equal':
            print('Equal:\nThe sections Line[%d:%d] of old and Line[%d:%d] of new are the same\n' %
                  (d[edit_type][0], d[edit_type][1], d[edit_type][2], d[edit_type][3]))

        elif edit_type == 'Insert':
            if '\n'.join(d[edit_type][0]).strip() != '':
                print('Insert:\n%s from Line[%d:%d] of new into old at Line %d\n' %
                  ('\n'.join(d[edit_type][0]), d[edit_type][1], d[edit_type][2], d[edit_type][3]))
                try:
                    diff_str += ('After:\n%s\nInsert:\n%s\n' %
                                (s1[d[edit_type][3]], '\n'.join(d[edit_type][0])))
                except:
                    print("Something went wrong!!!")
                changed_line_cnt += len(d[edit_type][0])

        elif edit_type == 'Replace':
            print('Replace:\n\n%s\n\nfrom Line[%d:%d] of old with:\n\n%s\n\nfrom Line[%d:%d] of new\n' % ('\n'.join(
                d[edit_type][0]), d[edit_type][1], d[edit_type][2], '\n'.join(d[edit_type][3]), d[edit_type][4], d[edit_type][5]))
            diff_str += ('Replace:\n%s\nwith:\n%s\n' %
                         ('\n'.join(d[edit_type][0]), '\n'.join(d[edit_type][3])))
            changed_line_cnt += abs(len(d[edit_type][0])-len(d[edit_type][3]))

        else:
            print('Error: Unknown operation, something wrong here!')
            exit(0)

    print("\nTotal changed lines: %d\n" % changed_line_cnt)

    return diff_str, changed_line_cnt
