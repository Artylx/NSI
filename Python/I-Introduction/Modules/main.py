from resolution import solve

def get_infos():
    a = None
    while a is None:
        try:
            a = float(input("Etrez le coef a: "))
        except ValueError:
            a = None
            print("[ERROR VALUE]")
            print("")
        except Exception:
            print("OS Error")
            exit(1)
    b = None
    while b is None:
        try:
            b = float(input("Etrez le coef b: "))
        except ValueError:
            b = None
            print("[ERROR VALUE]")
            print("")
        except Exception:
            print("OS Error")
            exit(1)
    return a, b

if __name__ == "__main__":
    a, b = get_infos()
    
    print(f"Solution de l'équation {solve(a, b)}")
    input("")
