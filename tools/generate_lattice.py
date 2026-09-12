"""Generate browser correspondence/path data from the maintained Python tables."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from vortex.src.mythology.correspondences import NODES
from vortex.src.mythology.paths import PATH_LETTERS, PATH_MEANINGS

POSITIONS = [(50, 9), (79, 23), (21, 23), (79, 41), (21, 41),
             (50, 50), (79, 66), (21, 66), (50, 79), (50, 94)]
NAMES = {"maat": "Ma’at", "spider_woman": "Spider Woman"}


def generate():
    nodes = {}
    for (key, node), (x, y) in zip(NODES.items(), POSITIONS):
        display = lambda name: NAMES.get(name, name.replace('_', ' ').title()) if name else None
        nodes[key] = dict(id=key, pond=node.pond, pillar=node.pillar,
                          classicalGuide=display(node.classical_guide_id),
                          folkGuide=display(node.folk_guide_id),
                          ledgerFloor=node.ledger_floor, creationUnlock=node.creation_unlock,
                          x=x, y=y)
    paths = [dict(id=':'.join(sorted((a, b))), **{'from': a, 'to': b},
                  letter=letter, title=title, meaning=PATH_MEANINGS[letter])
             for a, b, letter, title in PATH_LETTERS]
    assert len(nodes) == 10 and len(paths) == len({p['id'] for p in paths}) == 22
    return json.dumps(dict(version=1, nodes=nodes, paths=paths), ensure_ascii=False, indent=2) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    target = ROOT / 'vortex/web/lattice-data.json'
    content = generate()
    if args.check:
        if not target.exists() or target.read_text() != content:
            sys.exit('Browser lattice is stale. Run npm run generate:lattice.')
        print('Canonical lattice matches: 10 offices, 22 streams.')
    else:
        target.write_text(content)
        print('Generated vortex/web/lattice-data.json')
