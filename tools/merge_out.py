import json
from formatter import per_line_entries

out_ids = set()
out_dupe_ids = set()
atlas_ids = {}

with open('temp_atlas.json', 'r', encoding='utf-8') as out_file:
	out_json = json.loads(out_file.read())

with open('../web/atlas.json', 'r', encoding='utf-8') as atlas_file:
	atlas_json = json.loads(atlas_file.read())

for i, entry in enumerate(atlas_json):
	atlas_ids[entry['id']] = i

for entry in out_json:
	if entry['id'] in out_ids:
		print(f"Entry {entry['id']} has duplicates! Please resolve this conflict. This will be excluded from the merge.")
		out_dupe_ids.add(entry['id'])
	out_ids.add(entry['id'])

for entry in out_json:
	if entry['id'] in out_dupe_ids:
		continue

	if 'edit' in entry and entry['edit']:
		assert entry['id'] in atlas_ids, "Edit failed! ID not found on Atlas."
		index = atlas_ids[entry['id']]

		assert index != None, "Edit failed! ID not found on Atlas."

		print(f"Edited {atlas_json[index]['id']} with {entry['edit']}")

		del entry['edit']
		atlas_json[index] = entry
	elif entry['id'] in atlas_ids:
		print(f"Edited {entry['id']} manually.")
		atlas_json[atlas_ids[entry['id']]] = entry
	else:
		print(f"Added {entry['id']}.")
		atlas_json.append(entry)

print('Writing...')
with open('../web/atlas.json', 'w', encoding='utf-8') as atlas_file:
	atlas_file.write(per_line_entries(atlas_json))

with open('../data/read-ids.txt', 'a', encoding='utf-8') as read_ids_file:
	with open('read-ids-temp.txt', 'r', encoding='utf-8') as read_ids_temp_file:
		read_ids_file.writelines(read_ids_temp_file.readlines())

print('All done.')