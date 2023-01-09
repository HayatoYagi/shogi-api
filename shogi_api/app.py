import json
import os
import shutil
import pexpect


def lambda_handler(event, context):
    try:
        shutil.copyfile("yaneuraou/YaneuraOu-by-gcc", "/tmp/YaneuraOu-by-gcc")
        os.mkdir("/tmp/eval")
        shutil.copyfile("yaneuraou/eval/nn.bin", "/tmp/eval/nn.bin")
        # print(subprocess.check_output(["ls","-al","/tmp"]).decode())
        os.chmod("/tmp/YaneuraOu-by-gcc", 0o755)
        # print(subprocess.check_output(["ls","-al","/tmp"]).decode())

        with open('/tmp/mylog.txt', 'w') as fout:
            proc = pexpect.spawn("/tmp/YaneuraOu-by-gcc", encoding="utf-8")
            proc.logfile_read = fout
            proc.send("""\
usi
setoption name EvalDir value /tmp/eval
setoption name MultiPV value 2
setoption name USI_Hash value 1800
isready
usinewgame
position startpos moves 7g7f 3c3d 2g2f
go
""")
            proc.expect(pexpect.TIMEOUT, timeout=2)
            proc.sendline("stop")
            proc.sendline("quit")
            proc.close()

        with open('/tmp/mylog.txt', 'r') as log:
            # for line in log.readlines():
            #     print(line)
            res = {
                "statusCode": 200,
                "body": json.dumps({
                    "message": log.readlines(),
                }),
            }
            # print(res)
            return res
    except Exception as e:
        print(e)
        # print(subprocess.check_output("dmesg | egrep -i -B100 'killed process'", shell=True))
