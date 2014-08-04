import optparse, socket

def parse(usage):
	p = OptionParse(usage)

	p.add_option(
		"-m", "--mode",
		type="choise",
		choises=["client", "server"],
		default="client",
		metavar="MODE",
		help='choose mode from "client" or "server"'
	)

	return p.parse_args()

def main():
	print("""\
	Remote Sekisan Python-remix
	Takumi Sueda, 2014
	""")

if __name__ == "__main__":
	main()