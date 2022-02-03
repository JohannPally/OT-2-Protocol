from opentrons import protocol_api
import color_mask

# metadata
metadata = {
    'protocolName': 'testprotocol',
    'author': 'Johann',
    'description': 'test protocol to test OT-2',
    'apiLevel': '2.11'
}

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):

    # labware
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', '2')
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', '1')

    # pipettes
    left_pipette = protocol.load_instrument(
         'p300_single', 'left', tip_racks=[tiprack])
    camera = protocol.load_instrument(
        'p300_single', 'right', tip_racks=[tiprack])

    # commands
    left_pipette.pick_up_tip()


    left_pipette.drop_tip()

def adjust_location(x, y, well, plate):
    center_location = plate[well].center()
    xp, yp = trans_px2pt(x,y)
    adjusted_location = center_location.move(plate.types.Point(x=1, y=1, z=1))
    return adjusted_location

def trans_px2pt(x,y):
    return x,y