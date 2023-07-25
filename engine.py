# Craciun Florin Cristian si Elias Milosi
# grupa 141
sigma, states, transitions, lista = [], [], [], []
states_symbols = set()  # numele starii este un set pt ca nu dorim sa avem duplicate
camera_curenta = "EH"


def start():
	fisier = input("Introduceti numele fisierului(joc.in): ")  # Citim numele fisierului cu configul
	with open(fisier, "r") as f:
		tag = '#'  # tag ia valorile "Sigma", "States", sau "Transitions"
		while ls := f.readline():  # ii atribuim lui ls linia curenta din fisier si verificam daca e nenula
			ls = ls.rstrip('\n').split()  # scoatem '\n' de la finalul stringului si separam cuvintele cu spatii
			# intre ele
			if ls[0] == '#':  # Daca primul element din linie este #, este comentariu si ignoram
				continue
			if ls[0] == 'Sigma:':  # Daca primu element din linie este Sigma:, actualizam valoarea lui tag
				tag = ls[0]
			elif ls[0] == 'States:':  # Daca primu element din linie este States:, actualizam valoarea lui tag
				tag = ls[0]
			elif ls[0] == 'Transitions:':  # Daca primu element din linie este Transitions:, actualizam valoarea lui tag
				tag = ls[0]
			elif tag == 'Sigma:':  # Daca tagul curent este Sigma, inseamna ca citim alfabetul pana dam de cuvantul
				# 'End'; 'End' inseamna ca s-a terminat partea de sigma
				if ls != ['End']:
					sigm(ls)
			elif tag == 'States:':  # Daca tagul curent este States, inseamna ca citim elemente din multimea starilor
				# pana dam de cuvantul 'End'
				if ls != ['End']:
					stat(ls)
			elif tag == 'Transitions:':  # Daca tagul curent este Transitions, inseamna ca citim elemente din multimea
				# tranzitiilor pana dam de cuvantul 'End'
				if ls != ['End']:
					trans(ls)
	# Dupa ce am preluat informatia din config file, verificam daca alcatuieste un dfa
	return validare()


# Functia pentru citirea unei tranzitii
def trans(linie):
	global transitions
	if linie[3] == '-':  # Acceptam doar tranzitiile care au cratima intre ele, altfel nu sunt valide
		# Adaugam in transitions un 2-tuplu format din doua elemente de tip 3-tuplu
		transitions.append(
			(
				(linie[0].rstrip(','), linie[1].rstrip(','), linie[2]),  # parsam prima tranzitie
				(linie[4].rstrip(','), linie[5].rstrip(','), linie[6])  # parsam a doua tranzitie
			)
		)


# Functia pentru citirea unui element din alfabet
def sigm(linie):
	global sigma
	sigma.append(linie[0])  # Luam doar primul element din lista deoarece un element din alfabet este format dintr-un


# cuvant


# Functia pentur citirea unui element din multimea starilor
def stat(linie):
	global states
	try:
		states.append((linie[0].rstrip(','), linie[1]))  # Daca starea este notata ca stare de inceput('S') sau de
	# final ('F') atunci adaugam un 2-tuplu format din numele starii si 'S' sau 'F'
	except IndexError:
		states.append((linie[0].rstrip(','), -1))  # Daca starea nu este notata ca stare de inceput sau de final,


# in loc de 'S' sau 'F' scriem -1 ca sa marcam ca nu este nici de inceput, nici de final


def go(cuvant):
	global camera_curenta
	# Setam starea de inceput ca fiind mereu q1
	if cuvant not in states_symbols:
		# daca elementul nu e in alfabet atunci nu se potriveste dfa-ului
		input_gresit()
		return False
	for t in transitions:  # trecem prin fiecare tranzitie
		if t[0][0] == camera_curenta and cuvant == t[0][1]:  # verificam daca tranzitia are ca stare,starea noastra
			# curenta si daca elementul a1 este = cu litera la care ne situam in cuvantul citit
			# In tranzitia (q1, a1, s1) → (q2, a2, a3) verific daca exista s1 in lista
			if t[0][2] != "epsilon":
				if t[0][2] not in lista:
					print("Nu detii item-ul necesar ca sa intri.")
					return False

			# In tranzitia (q1, a1, s1) → (q2, a2, a3) il sterg pe a2 din lista, daca exista
			if t[1][1] != "epsilon":
				try:
					lista.remove(t[1][1])
				except ValueError:
					print(f"Elementul {t[1][1]} nu a putut fi sters din lista pentru ca nu exista")

			if t[1][2] != "epsilon" and t[1][2] not in lista:
				lista.append(t[1][2])  # adaugam a3 in lista din tranzitia de mai sus
			camera_curenta = t[1][0]  # modificam starea curenta la q2 din tranzitia de mai sus
			break
	else:
		print("Nu poti intra in aceasta camera.")


def input_gresit():
	print("Input-ul nu trece prin LA.")


def validare():
	global sigma, states, transitions, states_symbols
	s_counter = 0  # In aceasta variabila numaram cate stari sunt marcate cu 'S', adica sunt de inceput
	# fac o multime cu numele starilor si verific daca exista doar o stare de start
	for s in states:
		states_symbols.add(s[0])
		if s[1] == 'S':  # verificam daca starea este marcata cu S adica de inceput,si actualizam counterul
			s_counter += 1
	if s_counter > 1:  # Daca exista mai mult decat o stare de inceput atunci este gresit
		gresit()
		print("counter")
		return False

	# verific daca starile si literele exista
	for t in transitions:
		if t[0][0] not in states_symbols or t[1][0] not in states_symbols:  # verificam daca starile se gasesc in
			# multimea starilor
			gresit()
			return False
		if t[0][1] not in sigma and t[0][2] not in sigma and t[1][1] not in sigma and t[1][2] not in sigma:
			# verificam daca restul elementelor din tranzitie se gasesc in alfabet
			gresit()
			return False
	print("Automata este corecta")
	return True


def gresit():
	print("Automata este gresita")


if not start():
	exit(0)


info = {
	"EH": "The grand foyer of the Castle of Illusion",
	"DR": "A room with a large table filled with an everlasting fea",
	"K": "A room packed with peculiar ingredients",
	"A": "A chamber filled with antiquated weapons and armor",
	"T": "A glittering room overflowing with gold and gemstone",
	"L": "A vast repository of ancient and enchanted text",
	"P": "A storage area for the Kitchen.",
	"TR": "The command center of the castl",
	"WS": "A room teeming with mystical artifacts.",
	"SE": "The hidden passage that leads out of the Castle of Illusion"
}

obiecte_camere = {
	"EH": ["key"],
	"DR": ["invitation", "chefhat"],
	"K": ["spoon"],
	"A": ["sword", "crown"],
	"T": ["ancient_coin"],
	"L": ["spell_book"],
	"P": [],
	"TR": [],
	"WS": ["magic_wand"],
	"SE": []
}
	
while camera_curenta != "SE":
	print("\n[room name] can be: Entrance Hall = EH; Dining Room = DR; Kitchen = K; Armoury = A; Treasury = T, Library = L, Pantry = P; Throne Room = TR; Wizard's Study = WS; Secret Exit = SE")
	print("\n[item] can be: key = key; invitation = invitation; chef's hat = chefhat; spoon = spoon; sword = sword; crown = crown; ancient coin = ancient_coin; spell book = spell_book; magic wand = magic_wand\n")
	option = input(">>> Type a command (go [room name]/look/inventory/take [item]/ drop [item]/exit): ")
	option = option.split()
	if option[0] == "inventory":
		print(lista)
	elif option[0] == "go":
		go(option[1])
	elif option[0] == "look":
		print(f"Camera curenta:\n{camera_curenta}: {info[camera_curenta]}")
		print(f"Obiecte in camera curenta: {obiecte_camere[camera_curenta]}")
		print("Camerele adiacente:")
		for t in transitions:
			if t[0][0] == camera_curenta:  # Daca camera curenta din tranzitie este aceeasi cu cea a jucatorului
				print(f"{t[0][1]}: {info[t[0][1]]}")  # afisez informatii despre cele adiacente
		print()
	elif option[0] == "take":
		if option[1] in obiecte_camere[camera_curenta]:
			if option[1] not in lista:
				lista.append(option[1])
				obiecte_camere[camera_curenta].remove(option[1])  # Sterg obiectul din camera pentru ca a fost luat
			else:
				print("Ai obiectul deja in inventar.")
		else:
			print("Obiectul nu se afla in camera aceasta.")
	elif option[0] == "drop":
		if option[1] in lista:
			lista.remove(option[1])
			obiecte_camere[camera_curenta].append(option[1])
	elif option[0] == "exit":
		exit(0)
	if camera_curenta == "SE":
		print("Felicitari! Ai castigat!")
		break




