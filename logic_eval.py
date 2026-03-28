#!/usr/bin/env python3
"""Boolean logic — evaluate expressions, generate truth tables."""
import sys, re, itertools
def truth_table(expr, vars_list):
    print("  " + "  ".join(vars_list) + "  | Result")
    print("  " + "-"*(len(vars_list)*4+9))
    for vals in itertools.product([False,True], repeat=len(vars_list)):
        env={v:val for v,val in zip(vars_list,vals)}
        e=expr
        for v in vars_list: e=e.replace(v, str(env[v]))
        e=e.replace("AND","and").replace("OR","or").replace("NOT","not").replace("XOR","^").replace("NAND","not and")
        try: result=eval(e)
        except: result="ERR"
        vals_str="  ".join(str(int(v)) for v in vals)
        print(f"  {vals_str}  |   {int(result) if isinstance(result,bool) else result}")
def cli():
    if len(sys.argv)<2: print("Usage: logic_eval <expr> [vars]\n  e.g. 'A AND B OR NOT C' A B C"); sys.exit(1)
    expr=sys.argv[1]; vars_list=sys.argv[2:] if len(sys.argv)>2 else sorted(set(re.findall(r"[A-Z]",expr)))
    truth_table(expr, vars_list)
if __name__=="__main__": cli()
