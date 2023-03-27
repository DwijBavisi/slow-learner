import src.que as que
import src.utils.fingerprint as fp

for i, txt in enumerate(que.deq(1)):
    with open(f'corpus/{fp.get_hash(txt)}.html', 'w') as file:
        file.write(txt)
