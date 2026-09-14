from pathlib import Path
import re
import sys
from runtime import atomic_json,digest,entry,files,inside,parser,read_json

ALGORITHMS={'sha256':64,'sha512':128,'sha1':40,'md5':32}

def manifest(root,algorithm='sha256'):
    if algorithm not in ALGORITHMS:raise ValueError('Algorytm.')
    root=Path(root).resolve();entries={}
    for path in files(root):
        before=path.stat();value=digest(path,algorithm);after=path.stat()
        if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):raise ValueError('Plik zmieniony w trakcie odczytu.')
        entries[path.relative_to(root).as_posix()]={'hash':value,'size':before.st_size,'mtime_ns':before.st_mtime_ns}
    return dict(schema_version=1,algorithm=algorithm,files=entries)

def validate(value):
    if not isinstance(value,dict) or value.get('schema_version')!=1 or value.get('algorithm') not in ALGORITHMS or not isinstance(value.get('files'),dict):raise ValueError('Nieprawidłowy manifest.')
    for name,row in value['files'].items():
        inside('.',name)
        if not isinstance(row,dict) or not re.fullmatch('[a-fA-F0-9]{'+str(ALGORITHMS[value['algorithm']])+'}',str(row.get('hash',''))):raise ValueError('Nieprawidłowy hash.')
    return value

def compare(before,after):
    validate(before);validate(after)
    if before['algorithm']!=after['algorithm']:raise ValueError('Różne algorytmy.')
    a=before['files'];b=after['files']
    new=sorted(b.keys()-a.keys());missing=sorted(a.keys()-b.keys())
    changed=sorted(k for k in a.keys()&b.keys() if a[k]['hash'].lower()!=b[k]['hash'].lower())
    unchanged=sorted(k for k in a.keys()&b.keys() if k not in changed)
    return dict(new=new,missing=missing,changed=changed,unchanged=unchanged,ok=not(new or missing or changed))

def build():
    p=parser('Hashe i manifesty. SHA1/MD5 tylko kompatybilność.')
    p.add_argument('command',nargs='?',choices=['file','generate','verify','compare','compare-folders'])
    p.add_argument('--root');p.add_argument('--file');p.add_argument('--manifest');p.add_argument('--other')
    p.add_argument('--algorithm',choices=ALGORITHMS,default='sha256')
    return p

def handle(a):
    if a.command=='file':
        if not a.file:raise ValueError('Podaj --file.')
        return {'algorithm':a.algorithm,'hash':digest(a.file,a.algorithm)}
    if a.command=='generate':
        if not a.root or not a.manifest:raise ValueError('Podaj --root i --manifest.')
        root=Path(a.root).resolve();out=Path(a.manifest).resolve()
        if out.is_relative_to(root):raise ValueError('Manifest musi być poza badanym katalogiem.')
        if out.exists():raise FileExistsError(out)
        data=manifest(root,a.algorithm);atomic_json(out,data);return data
    if a.command=='verify':
        if not a.root or not a.manifest:raise ValueError('Podaj --root i --manifest.')
        before=validate(read_json(a.manifest));return compare(before,manifest(a.root,before['algorithm']))
    if a.command=='compare-folders':
        if not a.root or not a.other:raise ValueError('Podaj --root i --other jako foldery.')
        return compare(manifest(a.root,a.algorithm),manifest(a.other,a.algorithm))
    if a.command=='compare':
        if not a.manifest or not a.other:raise ValueError('Podaj dwa manifesty.')
        return compare(read_json(a.manifest),read_json(a.other))
    raise ValueError('Wybierz polecenie.')

if __name__=='__main__':sys.exit(entry(build,handle))
