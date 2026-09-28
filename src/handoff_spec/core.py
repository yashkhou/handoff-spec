import hashlib,json
REQUIRED=('version','objective','completed','evidence','unresolved','authority','invariants','next')
class HandoffError(ValueError): pass
def validate(d):
    missing=[k for k in REQUIRED if k not in d]
    if missing: raise HandoffError('missing: '+','.join(missing))
    if d['version']!='1': raise HandoffError('unsupported version')
    for k in ('completed','evidence','unresolved','invariants','next'):
        if not isinstance(d[k],list): raise HandoffError(f'{k} must be a list')
    if not isinstance(d['objective'],str) or not d['objective'].strip(): raise HandoffError('objective must be non-empty')
    a=d['authority']
    if not isinstance(a,dict) or not isinstance(a.get('allowed'),list) or not isinstance(a.get('forbidden'),list): raise HandoffError('authority requires allowed/forbidden lists')
    overlap=set(a['allowed']) & set(a['forbidden'])
    if overlap: raise HandoffError('authority conflict: '+','.join(sorted(overlap)))
    if not d['invariants']: raise HandoffError('at least one continuation invariant is required')
    return d
def canonical(d): validate(d); return json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(d): return hashlib.sha256(canonical(d).encode()).hexdigest()
