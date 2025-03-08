while [ ! -z "$1" ]; do
	case "$1" in
		--clean)
			rm -rf venv_3.12
			shift
			;;

		--tools)
			installTools=1
			shift
			;;

		--shell)
			runShell=1
			shift
			;;

		--fixup_pyodbc)
			fixup=1
			shift
			;;

		*)
			echo "Usage: $0 [--clean] [--tools] [--shell] [--fixup_pyodbc]"
			echo

			exit 10
			;;
    esac

done


rm -f venv
python3.12 -m venv venv_3.12
ln -sf venv_3.12 venv

source venv/bin/activate

pip3.12 install -r requirements.txt