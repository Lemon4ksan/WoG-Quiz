def fix_it(name: str) -> str | None:
    """
    Attempts to fix wrong text recognition. There will be more fixes later on.
    :Note: Probably should be implemented better
    """
    if name == "":
        return  # Nothing was found

    # Multiple weapons fixes ↓
    if name[-1] in (".", ",", ":", "~", "“"):  # Make sure to take this into account when creating fixes
        name = name.replace(name[-1], "")
    if name[0] in (".", ",", ":", "~", "“"):
        name = name.replace(name[0], "")
    if "Il" in name:
        name = name.replace("l", "I")

    # Doesn't exist in the guide ↓
    elif "zis" in name:
        return
    elif "Flak" in name:
        return
    elif "TKB-022PM" in name:
        return
    elif "Villar Perosa" in name:
        return
    elif "Ithaca 37" in name:
        return

    # Single weapon fixes ↓
    if "CZ" in name and "7" in name:  # rare typo <"CZ-5" in name> will break things if CZ-52 will appear
        name = "CZ-75"
    elif "CZ52" in name:
        name = "CZ-52"
    elif "type b" in name.lower():  # The guide was right (why is it named Type B in quiz?)
        name = "Stryk B"
    elif "BAR" in name:
        name = "B.A.R."
    elif "1919.04" in name:
        name = "M1919 A4"
    elif "Berdan" in name:
        name = "Berdan 2"
    elif "vz61" in name:
        name = "VZ 61"
    elif "M1944" in name:
        name = name.replace("44", "41")
    elif name == "MG3":
        name = "MG 3"
    elif name == "14":
        name = "M14"
    elif "Model 2" in name:
        name = "Model 21"
    elif "ART" in name:
        name = "AR-7"
    elif "S&W" in name:
        name = "S&W M&P"
    elif "HK 3303" in name:
        name = "HK 33A3"
    elif "1T" in name:
        name = "TT"
    # elif "Ruger MK" in name:  # Uncomment in case if <elif "Il" in name:> doesn't work
    #     name = "Ruger MK II"
    elif "M240" in name:
        name = "M240B"
    elif "K3" in name:
        name = "K31"
    elif "v2" in name and "2" in name:
        name = "vz.52"
    elif "v2" in name and "8" in name:
        name = "vz.58"
    elif "M16" in name:
        name = "M16 A1"
    elif "MpP" in name:
        print(name)
        name = "MP40"
    elif "Luger P" in name:
        name = "Luger P08"
    elif "CZ805" in name:
        name = "CZ 805 BREN"
    elif "FN5" in name:
        name = "FN 57"
    elif "Ruger Precision" in name:  # why won't it read entire name?
        name = "Ruger Precision Rifle"
    elif "SW Si" in name:
        name = "S&W Sigma"
    elif "Le6A" in name:
        name = "L86A2"
    elif "MAS 4" in name:
        name = "MAS 49/56"
    elif "9.A4" in name:
        name = "M1919 A4"
    elif "Lee" in name:
        name = "L86A2"
    elif "Browning A" in name:
        name = "Browning A5"
    elif "T0z-" in name:
        name = "TOZ-34"
    elif "OsvV" in name:
        name = "OSV-96"
    elif "Remington R5" in name:
        name = "Remington R51"
    elif "HK PS" in name:
        name = "HK PSG1"
    elif "S8W Sc" in name:
        name = "S&W Schofield"
    elif "SKS M5" in name:
        name = "SKS M59/66"
    elif "SVT" in name:
        name = "SVT-40"
    return name

if __name__ == '__main__':
    name_ = "HK PSG14"
    print(fix_it(name_))
