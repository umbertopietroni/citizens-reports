


def predict_issue(text_dict, image_dict_list):
    if image_dict_list:
        i = 0
        ambiente,illuminazione,manutenzione,sicurezza = 0,0,0,0
        for image_dict in image_dict_list:
            i += 1
            ambiente += float(image_dict["ambiente"])
            illuminazione += float(image_dict["illuminazione"])
            manutenzione += float(image_dict["manutenzione"])
            sicurezza += float(image_dict["sicurezza"])
        if (i!=0):
            ambiente = ambiente/i
            illuminazione = illuminazione/i
            manutenzione = manutenzione/i
            sicurezza = sicurezza/i
        new_dict = {}
        if text_dict:
            new_dict["ambiente"] = (float(text_dict["ambiente"])+ambiente) / 2
            new_dict["manutenzione"] = (float(text_dict["manutenzione"])+manutenzione) / 2
            new_dict["illuminazione"] = (float(text_dict["illuminazione"])+illuminazione) / 2
            new_dict["sicurezza"] = (float(text_dict["sicurezza"])+sicurezza) / 2
        else:
            new_dict["ambiente"] = ambiente
            new_dict["manutenzione"] = manutenzione
            new_dict["illuminazione"] = illuminazione
            new_dict["sicurezza"] = sicurezza
        
        
        #print("testo",text_dict)
        #print( ambiente,illuminazione,manutenzione,sicurezza)
        print(new_dict)
        category = list(new_dict.keys())[list(new_dict.values()).index(max(new_dict.values()))]
        return category
        
    else:
        category = list(text_dict.keys())[list(text_dict.values()).index(max(text_dict.values()))]
        return category
