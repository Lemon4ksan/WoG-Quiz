def fix_it(name: str) -> str | None:
    """
    Attempts to fix wrong text recognition. There will be more fixes later on.
    :Note: Probably should be implemented better
    """
    if name == "" or name == "Close":
        return  # Nothing was found or quiz was finished

    # Multiple weapons fixes ↓
    if name[-1] in (".", ",", ":", "~", "“"):  # Make sure to take this into account when creating fixes
        name = name.replace(name[-1], "")
    if name[0] in (".", ",", ":", "~", "“"):
        name = name.replace(name[0], "")
    if "~" in name:
        name = name.replace("~", "-")
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
    elif "Type B" in name:
        return  # Not sure ?? This literally put me 2 buttons with Type B and Stryk B, the second one was right ??

    # Single weapon fixes ↓
    if name == "MG3":
        return "MG 3"
    elif name == "14":
        return "M14"
    elif name == "Ms":
        return "M4"
    elif name == "PP-49":
        return "PP-19"
    elif "S8&W 4" in name:
        return "S&W 4006"
    elif "CZ" in name and "7" in name:  # rare typo <"CZ-5" in name> will break things if CZ-52 will appear
        return "CZ-75"
    elif "CZ52" in name:
        return "CZ-52"
    # elif "type" in name.lower():  # The guide was right (why is it named Type B in quiz?)
    #     return "Stryk B"
    elif "BAR" in name:
        return "B.A.R."
    elif "1919" in name:
        return "M1919 A4"
    elif "Berdan" in name:
        return "Berdan 2"
    elif "vz61" in name:
        return "VZ 61"
    elif "M1944" in name:
        name = name.replace("44", "41")
    elif "Model 24" in name:
        return "Model 21"
    elif "ART" in name:
        return "AR-7"
    elif "S&W" in name:
        return "S&W M&P"
    elif "HK 3303" in name:
        return "HK 33A3"
    elif "1T" in name:
        return "TT"
    elif "M240" in name:
        return "M240B"
    elif "K3" in name:
        return "K31"
    elif "v2" in name and name[-1] == "2":
        return "vz.52"
    elif "v2" in name and name[-1] == "8":
        return "vz.58"
    elif "M16" in name:
        return "M16 A1"
    elif "MpP" in name:
        return "MP40"
    elif "Luger P" in name:
        return "Luger P08"
    elif "CZ805" in name:
        return "CZ 805 BREN"
    elif "FN5" in name:
        return "FN 57"
    elif "Ruger Precision" in name:  # why won't it read entire name?
        return "Ruger Precision Rifle"
    elif "SW Si" in name:
        return "S&W Sigma"
    elif "Le6A" in name:
        return "L86A2"
    elif "MAS 4" in name:
        return "MAS 49/56"
    elif "9.A4" in name:
        return "M1919 A4"
    elif "Lee" in name:
        return "L86A2"
    elif "Browning A" in name:
        return "Browning A5"
    elif "T0z-" in name:
        return "TOZ-34"
    elif "OsvV" in name:
        return "OSV-96"
    elif "Remington R5" in name:
        return "Remington R51"
    elif "HK PS" in name:
        return "HK PSG1"
    elif "S8W Sc" in name:
        return "S&W Schofield"
    elif "SKS M5" in name:
        return "SKS M59/66"
    elif "SVT" in name:
        return "SVT-40"
    elif "Wreten" in name:
        return "Welrod"
    elif "SG510" in name:
        return "SIG SG 510"
    elif "Suomi KP" in name:
        return "Suomi KP/-31"

    return name

if __name__ == '__main__':
    name_ = "Bren MKIl"
    print(fix_it(name_))
