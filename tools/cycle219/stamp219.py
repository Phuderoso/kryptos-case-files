"""Cycle 219 results-file convention (fix adopted in PREREG219 Part B).
Every results file starts with '#' header lines naming its scope and the exact inputs, so two zero-hit outputs of different texts
can never be byte-identical again.
usage: stamp219.py OUT SCOPE TEXTLABEL CT TOOLSRC SEED ARGS... < body   (writes header + body to OUT)"""
import hashlib, sys
def sha(b): return hashlib.sha256(b).hexdigest()
def header(scope,label,ct,toolsrc,seed,args):
    return [f"# scope={scope}", f"# text={label} input_sha256={sha(ct.encode())} (97-letter string, no newline)",
            f"# tool={toolsrc} tool_sha256={sha(open(toolsrc,'rb').read())}", f"# seed={seed} args={' '.join(args)}"]
if __name__=="__main__":
    out,scope,label,ct,toolsrc,seed=sys.argv[1:7]
    body=sys.stdin.read()
    with open(out,"w") as f: f.write("\n".join(header(scope,label,ct,toolsrc,seed,sys.argv[7:]))+"\n"+body)
