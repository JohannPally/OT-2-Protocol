import requests  # you can install this with pip


def run(protocol):
    tiprack = protocol.load_labware('opentrons_tiprack_300ul', '1')
    trough = protocol.load_labware('nest_12_reservoir_15ml', '2')
    pipette = protocol.load_instrument('p300_single', 'right', tip_racks=[tiprack])

    pipette.pick_up_tip()
    pipette.aspirate(10, trough.wells()['A1'])

    done = False  # Poll to see if the server wants you to proceed
    while not done:
        r = requests.post('http://127.0.0.1/update', json={'step': 'done-aspirating'})
        done = r.json()['done']

    pipette.dispense()