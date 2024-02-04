import FreeCAD as App
import Part

# Alles löschen
for obj in App.activeDocument().Objects:
    App.activeDocument().removeObject(obj.Name)
App.activeDocument().recompute()


# Definiere die Abmessungen der Grundfläche
grundflaeche_laenge = 80  # Länge in mm
grundflaeche_breite = 80  # Breite in mm
grundflaeche_dicke = 2    # Dicke in mm
wand_hoehe = 40           # Höhe der Seitenwände in mm
seitenwand_dicke = 4
fuehrungsschiene_dicke = 2  # Dicke der Führungsschienen in mm
fuehrungsschiene_hoehe = 2  # Höhe der Führungsschienen in mm
mutternkiste_breite = 5     # Breite/Länge der Mutternkiste
gewindeloch_durchmesser = 2 # Durchmesser der Löcher in der Mutternkiste
schraubenloch_durchmesser = 3 # Durchmesser der Löcher in der Seitenwand zum Schrauben durchstecken
lueftungsschlitzlaenge = 10
schlitzabstand = 4
display_breite = 19.5 # y-Richtung
display_laenge = 27.5 # x-Richtung


# Erstelle die Grundfläche (Box)
grundflaeche = Part.makeBox(grundflaeche_laenge, grundflaeche_breite, grundflaeche_dicke)


def getSchraubennest(mutternkiste_breite=mutternkiste_breite, mutternkiste_hoehe = mutternkiste_breite):
    # Erstelle die Box für das Schraubennest
    schraubennest = Part.makeBox(mutternkiste_breite, mutternkiste_breite, mutternkiste_hoehe)

    # Erstelle den Zylinder für das Gewinde
    schraubengewinde = Part.makeCylinder(gewindeloch_durchmesser / 2, mutternkiste_breite)
    schraubengewinde.translate(App.Vector(mutternkiste_breite/2, mutternkiste_breite / 2, 0))

    # Schneide den Zylinder aus der Box
    schraubennest = schraubennest.cut(schraubengewinde)
    return schraubennest



# Liste der Erhebungen mit x, y Positionen
x1 = 13
x2 = x1 + 54
y1 = 10
y2 = y1 + 54
y3 = y1 + 29

erhebungen = [
    {"x": x1, "y": y1, "durchmesser1": 4, "durchmesser2": 2, "hoehe": 6},
    {"x": x2, "y": y1, "durchmesser1": 4, "durchmesser2": 2, "hoehe": 6},
    {"x": x1, "y": y2, "durchmesser1": 4, "durchmesser2": 2, "hoehe": 6},
    {"x": x2, "y": y2, "durchmesser1": 4, "durchmesser2": 2, "hoehe": 6}
]

schraubenloecher = [
    {"x": x1, "y": y3, "durchmesser1": 6, "durchmesser2": 1.8, "hoehe": 6},
    {"x": x2, "y": y3, "durchmesser1": 6, "durchmesser2": 1.8, "hoehe": 6}
]

# Erstelle die einzelnen runden Erhebungen
for erhebung in erhebungen:
    z_position = grundflaeche_dicke / 2 + erhebung["hoehe"] / 2
    cylinder1 = Part.makeCylinder(erhebung["durchmesser1"] / 2, erhebung["hoehe"])
    cylinder1.translate(App.Vector(erhebung["x"], erhebung["y"], 0))
    cylinder2 = Part.makeCylinder(erhebung["durchmesser2"] / 2, erhebung["hoehe"] - 4)
    cylinder2.translate(App.Vector(erhebung["x"], erhebung["y"], grundflaeche_dicke + 4))  # Höhe - 4 mm für die letzten 2 mm
    grundflaeche = grundflaeche.fuse(cylinder1)
    grundflaeche = grundflaeche.fuse(cylinder2)

for erhebung in schraubenloecher:
    z_position = grundflaeche_dicke / 2 + erhebung["hoehe"] / 2
    cylinder1 = Part.makeCylinder(erhebung["durchmesser1"] / 2, erhebung["hoehe"])
    cylinder1.translate(App.Vector(erhebung["x"], erhebung["y"], 0))
    cylinder2 = Part.makeCylinder(erhebung["durchmesser2"] / 2, erhebung["hoehe"])
    cylinder2.translate(App.Vector(erhebung["x"], erhebung["y"], 0))
    cylinder1 = cylinder1.cut(cylinder2)
    grundflaeche = grundflaeche.fuse(cylinder1)
    #grundflaeche = grundflaeche.fuse(cylinder2)



schraubennest_links_unten = getSchraubennest()
#Rotiere um die Z-Achse um 45 Grad
schraubennest_links_unten.rotate(App.Vector(mutternkiste_breite/2, mutternkiste_breite/2, mutternkiste_breite/2), App.Vector(1, 0, 0), 90)
schraubennest_links_unten.rotate(App.Vector(mutternkiste_breite/2, mutternkiste_breite/2, mutternkiste_breite/2), App.Vector(0, 0, 1), 90)
schraubennest_links_unten.translate(App.Vector(grundflaeche_dicke, grundflaeche_dicke, grundflaeche_dicke))

schraubennest_links_oben = schraubennest_links_unten.copy()
schraubennest_links_oben.translate(App.Vector(0, grundflaeche_breite - 2*grundflaeche_dicke - mutternkiste_breite,0))

schraubennest_rechts_oben = schraubennest_links_oben.copy()
schraubennest_rechts_oben.translate(App.Vector(grundflaeche_laenge - 2* grundflaeche_dicke - mutternkiste_breite,0))

schraubennest_rechts_unten = schraubennest_links_unten.copy()
schraubennest_rechts_unten.translate(App.Vector(grundflaeche_laenge - 2* grundflaeche_dicke - mutternkiste_breite,0))
# Schraubennest der Grundfläche hinzufügen
grundflaeche = grundflaeche.fuse(schraubennest_links_unten)
grundflaeche = grundflaeche.fuse(schraubennest_links_oben)
grundflaeche = grundflaeche.fuse(schraubennest_rechts_oben)
grundflaeche = grundflaeche.fuse(schraubennest_rechts_unten)

## Untere Wand
wand_unten = Part.makeBox(grundflaeche_laenge, grundflaeche_dicke, wand_hoehe)
wand_unten.translate(App.Vector(0,0,grundflaeche_dicke))
grundflaeche = grundflaeche.fuse(wand_unten)

## Linke Seitenwand
wand_links = Part.makeBox(grundflaeche_dicke, grundflaeche_breite - 2 * grundflaeche_dicke, wand_hoehe)
wand_links.translate(App.Vector(0,grundflaeche_dicke,grundflaeche_dicke))
# unteres Schraubenloch
schraubenloch_links_unten = Part.makeCylinder(schraubenloch_durchmesser/2, grundflaeche_dicke)
schraubenloch_links_unten.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)
schraubenloch_links_unten.translate(App.Vector(0, mutternkiste_breite / 2 + grundflaeche_dicke, grundflaeche_dicke + mutternkiste_breite / 2))
wand_links = wand_links.cut(schraubenloch_links_unten)
# oberes Schraubenloch
schraubenloch_links_oben = Part.makeCylinder(schraubenloch_durchmesser/2, grundflaeche_dicke)
schraubenloch_links_oben.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)
schraubenloch_links_oben.translate(App.Vector(0, grundflaeche_breite - mutternkiste_breite / 2 - grundflaeche_dicke, grundflaeche_dicke + mutternkiste_breite / 2))
wand_links = wand_links.cut(schraubenloch_links_oben)

# Führungsschiene mit Schräge links
dreieck = Part.makePolygon([App.Vector(grundflaeche_dicke, grundflaeche_dicke, wand_hoehe + grundflaeche_dicke), App.Vector(grundflaeche_dicke*2, grundflaeche_dicke, wand_hoehe + grundflaeche_dicke), App.Vector(grundflaeche_dicke, grundflaeche_dicke, wand_hoehe)], True)
prisma = Part.Face(dreieck).extrude(App.Vector(0, grundflaeche_breite - 2 * grundflaeche_dicke, 0))
schienen_rueckseite = Part.makeBox(grundflaeche_dicke, grundflaeche_breite - 2 * grundflaeche_dicke, grundflaeche_dicke)
schienen_rueckseite.translate(App.Vector(grundflaeche_dicke, grundflaeche_dicke, wand_hoehe - 2 * grundflaeche_dicke))
wand_links = wand_links.fuse(prisma)
#wand_links = wand_links.fuse(schienen_rueckseite)

# Lüftungsschlitze rechts
x =  0
wand = wand_links
for i1 in range(0, 4):
    for i0 in range(0, 4):
        lueftungsschlitz = Part.makeBox(grundflaeche_dicke, lueftungsschlitzlaenge, grundflaeche_dicke)
        lueftungsschlitz.translate(App.Vector(x, 3* grundflaeche_dicke + i1*(2 * schlitzabstand + lueftungsschlitzlaenge), 5 * grundflaeche_dicke + i0*schlitzabstand))
        wand = wand.cut(lueftungsschlitz)
wand_links = wand



## Rechte Seitenwand
wand_rechts = Part.makeBox(grundflaeche_dicke, grundflaeche_breite - 2 * grundflaeche_dicke, wand_hoehe)
wand_rechts.translate(App.Vector(grundflaeche_laenge - grundflaeche_dicke,grundflaeche_dicke,grundflaeche_dicke))
# unteres Schraubenloch
schraubenloch_rechts_unten = Part.makeCylinder(schraubenloch_durchmesser/2, grundflaeche_dicke)
schraubenloch_rechts_unten.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)
schraubenloch_rechts_unten.translate(App.Vector(grundflaeche_laenge - grundflaeche_dicke, mutternkiste_breite / 2 + grundflaeche_dicke, grundflaeche_dicke + mutternkiste_breite / 2))
wand_rechts = wand_rechts.cut(schraubenloch_rechts_unten)
# oberes Schraubenloch
schraubenloch_rechts_oben = Part.makeCylinder(schraubenloch_durchmesser/2, grundflaeche_dicke)
schraubenloch_rechts_oben.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)
schraubenloch_rechts_oben.translate(App.Vector(grundflaeche_laenge - grundflaeche_dicke, grundflaeche_breite - mutternkiste_breite / 2 - grundflaeche_dicke, grundflaeche_dicke + mutternkiste_breite / 2))
wand_rechts = wand_rechts.cut(schraubenloch_rechts_oben)
# Führungsschiene mit Schräge rechts
dreieck = Part.makePolygon([App.Vector(grundflaeche_laenge - 2 * grundflaeche_dicke, grundflaeche_dicke, wand_hoehe + grundflaeche_dicke), App.Vector(grundflaeche_laenge - grundflaeche_dicke, grundflaeche_dicke, wand_hoehe + grundflaeche_dicke), App.Vector(grundflaeche_laenge - grundflaeche_dicke, grundflaeche_dicke, wand_hoehe)], True)
prisma = Part.Face(dreieck).extrude(App.Vector(0, grundflaeche_breite - 2 * grundflaeche_dicke, 0))
schienen_rueckseite = Part.makeBox(grundflaeche_dicke, grundflaeche_breite - 2 * grundflaeche_dicke, grundflaeche_dicke)
schienen_rueckseite.translate(App.Vector(grundflaeche_laenge - 2 * grundflaeche_dicke, grundflaeche_dicke, wand_hoehe - 2 * grundflaeche_dicke))
wand_rechts = wand_rechts.fuse(prisma)
#wand_rechts = wand_rechts.fuse(schienen_rueckseite)

# Lüftungsschlitze rechts
x = grundflaeche_laenge - 1 * grundflaeche_dicke
wand = wand_rechts
for i1 in range(0, 4):
    for i0 in range(0, 4):
        lueftungsschlitz = Part.makeBox(grundflaeche_dicke, lueftungsschlitzlaenge, grundflaeche_dicke)
        lueftungsschlitz.translate(App.Vector(x, 3* grundflaeche_dicke + i1*(2 * schlitzabstand + lueftungsschlitzlaenge), 5 * grundflaeche_dicke + i0*schlitzabstand))
        wand = wand.cut(lueftungsschlitz)
wand_rechts = wand

# Loch für Kabel
kabelloch = Part.makeBox(grundflaeche_dicke, lueftungsschlitzlaenge, 3 * grundflaeche_dicke)
kabelloch.translate(App.Vector(x, 4* grundflaeche_dicke + lueftungsschlitzlaenge/2, 1 * grundflaeche_dicke))
wand_rechts = wand_rechts.cut(kabelloch)



## Deckel
deckel = Part.makeBox(grundflaeche_laenge, grundflaeche_breite, grundflaeche_dicke)
deckel.translate(App.Vector(0, 0, wand_hoehe + grundflaeche_dicke))
wand_oben = Part.makeBox(grundflaeche_laenge, grundflaeche_dicke, wand_hoehe)
wand_oben.translate(App.Vector(0,grundflaeche_breite - grundflaeche_dicke,grundflaeche_dicke))
deckel = deckel.fuse(wand_oben)

# Schwalbenschwanz rechts
dreieck = Part.makePolygon([
        App.Vector(grundflaeche_laenge - 3 * grundflaeche_dicke, grundflaeche_dicke, wand_hoehe + grundflaeche_dicke), 
        App.Vector(grundflaeche_laenge - 2 * grundflaeche_dicke -0.1, grundflaeche_dicke, wand_hoehe + grundflaeche_dicke), 
        App.Vector(grundflaeche_laenge - 1 * grundflaeche_dicke -0.1, grundflaeche_dicke, wand_hoehe), 
        App.Vector(grundflaeche_laenge - 3 * grundflaeche_dicke, grundflaeche_dicke, wand_hoehe)], True)
prisma = Part.Face(dreieck).extrude(App.Vector(0, grundflaeche_breite - 2 * grundflaeche_dicke, 0))
deckel = deckel.fuse(prisma)
# Schwalbenschwanz links
dreieck = Part.makePolygon([
        App.Vector(grundflaeche_dicke*2 + 0.1, grundflaeche_dicke, wand_hoehe + grundflaeche_dicke), 
        App.Vector(grundflaeche_dicke*3, grundflaeche_dicke, wand_hoehe + grundflaeche_dicke), 
        App.Vector(grundflaeche_dicke*3, grundflaeche_dicke, wand_hoehe),
        App.Vector(grundflaeche_dicke*1 + 0.1, grundflaeche_dicke, wand_hoehe)], True)
prisma = Part.Face(dreieck).extrude(App.Vector(0, grundflaeche_breite - 2 * grundflaeche_dicke, 0))
deckel = deckel.fuse(prisma)

## Displayhalterung im Deckel

# Loch für das Display selbst
display_loch = Part.makeBox(display_laenge, display_breite, grundflaeche_dicke)
display_loch.translate(App.Vector(grundflaeche_laenge/2, grundflaeche_breite/2 - display_breite, wand_hoehe + grundflaeche_dicke))
deckel = deckel.cut(display_loch)

# Muttern zur Befestigung des Displays
mutternkiste_breite_display = 4
mutternkiste_hoehe_display = 3
schraubennest_z = wand_hoehe + 0.9 # Wird in den Deckel versenkt.
schraubennest_y = grundflaeche_breite/2 - display_breite - mutternkiste_breite_display

display_schraubennest = getSchraubennest(mutternkiste_breite_display,mutternkiste_hoehe_display)
display_schraubennest.translate(App.Vector(grundflaeche_laenge/2, schraubennest_y, schraubennest_z))
deckel = deckel.fuse(display_schraubennest)
display_schraubennest = getSchraubennest(mutternkiste_breite_display,mutternkiste_hoehe_display)
display_schraubennest.translate(App.Vector(grundflaeche_laenge/2 + display_laenge - mutternkiste_breite_display, schraubennest_y, schraubennest_z))
deckel = deckel.fuse(display_schraubennest)

schraubennest_y = grundflaeche_breite/2
display_schraubennest = getSchraubennest(mutternkiste_breite_display,mutternkiste_hoehe_display)
display_schraubennest.translate(App.Vector(grundflaeche_laenge/2, schraubennest_y, schraubennest_z))
deckel = deckel.fuse(display_schraubennest)
display_schraubennest = getSchraubennest(mutternkiste_breite_display,mutternkiste_hoehe_display)
display_schraubennest.translate(App.Vector(grundflaeche_laenge/2 + display_laenge - mutternkiste_breite_display, schraubennest_y, schraubennest_z))
deckel = deckel.fuse(display_schraubennest)

# Aussparungen für Displaykabel und Lötanschluss
lochbreite = 4 # Y-Richtung
lochlaenge = 12 # X-Richtung
lochhoehe = 4 # Z-Richtung
loch_y = grundflaeche_breite/2 - display_breite - lochbreite # Y-Richtung
loch_z = wand_hoehe - 0.5
loch_x = grundflaeche_laenge/2 + mutternkiste_breite_display + (display_laenge - 2 * mutternkiste_breite_display - lochlaenge)/2
kabelloch = Part.makeBox(lochlaenge, lochbreite, lochhoehe)
kabelloch.translate(App.Vector(loch_x, loch_y, loch_z))
deckel = deckel.cut(kabelloch)

loch_y = grundflaeche_breite/2
loetloch = Part.makeBox(lochlaenge, lochbreite, lochhoehe)
loetloch.translate(App.Vector(loch_x, loch_y, loch_z))
deckel = deckel.cut(loetloch)

# Füge die modifizierte Grundfläche zum Dokument hinzu
App.activeDocument().addObject("Part::Feature", "Grundflaeche").Shape = grundflaeche

# Füge rechte Wand hinzu
App.activeDocument().addObject("Part::Feature", "Wand_Rechts").Shape = wand_rechts

# Füge linke Wand hinzu
App.activeDocument().addObject("Part::Feature", "Wand_links").Shape = wand_links


App.activeDocument().addObject("Part::Feature", "Deckel").Shape = deckel


# Zeige das Dokument an
App.activeDocument().recompute()
# Gui.SendMsgToActiveView("ViewFit")
