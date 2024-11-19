from flask import Flask, render_template, request ,redirect, url_for, session
from owlready2 import *
from datetime import datetime
from urllib.parse import unquote


# Load your ontology
ontology_path = "actual_owl_files/entended_protege.owl"
onto = get_ontology(ontology_path).load()

# Define inverse properties outside the function

#battery_to_UPS
onto.This_battery_is_backing_up_this_UPS.inverse=onto.This_UPS_is_being_backed_by_this_battery

#CMCB_to_socket
onto.This_socket_is_connected_to_this_MCB.inverse=onto.This_MCB_is_connected_to_this_socket

#DB_to_CMCB
onto.This_MCB_is_connected_to_this_DB.inverse=onto.This_DB_is_connected_to_this_MCB

#Diesel_generator_to_EB
onto.This_generator_is_backing_up_this_EB.inverse=onto.This_Eb_is_backed_by_this_generator

#EB_to_UPS
onto.This_UPS_is_being_powered_by_this_EB.inverse=onto.This_Eb_is_powering_this_UPS

#Zone_to_machine 
onto.This_zone_rack_and_position_has_the_machine.inverse=onto.This_machine_is_present_in_the_zone_rack_and_position

#Pdu_to_zone
onto.This_Rack_is_connectedto_this_PDU.inverse=onto.This_PDU_isconnectedto_the_rack

#Socket_to_pdu
onto.This_socket_is_connected_to_this_PDU.inverse=onto.This_PDU_is_connected_to_this_socket

#UPS_to_DB
onto.This_UPS_send_power_to_this_distribution_board.inverse=onto.This_Distribution_board_is_powered_by_this_UPS

#Machine_to_faculty
onto.This_person_owns_the_machine.inverse=onto.This_machine_belongs_to_the_person




def decode_form_data(form_data):
    decoded_data = {}
    for key, value in form_data.items():
        decoded_data[key] = unquote(value)
    return decoded_data




def create_ontology(zone_selection, rack_instance, rack_number, position_number, machine_instance, cpu_model, cpu_frequency_MHZ, date_install, host_name, machine_model, memory_GB, network_port_open, power_watts, ipv4_address, u_count, people_instance, department, email, phone_number, room_number, pdu_instance, socket_instance, CMCB_instance, DB_instance, UPS_instance, battery_instance):
    

    # individual properties
    #new_individual_zone=onto.Zone(zone_selection)
    #new_individual_zone_rack = getattr(onto, zone_selection)(rack_instance)

    zone_class = getattr(onto, zone_selection)  # Get the class, e.g., Zone_A
    new_individual_zone_rack = zone_class(rack_instance)  # Create individual


    #new_individual_rack = onto.Rack(rack_instance)
    new_individual_machine =  onto.Machine(machine_instance)
    new_individual_people = onto.Faculty(people_instance)
    new_individual_pdu=onto.Rack_PDU(zone_selection+"_"+rack_instance+"_"+pdu_instance)
    new_individual_socket=onto.Socket(socket_instance)
    new_individual_cmcb=onto.Connected_Miniature_Circuit_Breaker(zone_selection+"_"+DB_instance+"_"+"CMCB_"+CMCB_instance)
    new_individual_db=onto.Distribution_Board(zone_selection+"_"+DB_instance)
    new_individual_ups=onto.UPS("UPS_"+UPS_instance)
    new_individual_battery=onto.Battery("Battery_"+battery_instance)




    # Object properties
    # new_individual_rack.contains_machine.append(new_individual_machine)  # Rack has a machine
    # new_individual_machine.belongs_to.append(new_individual_people)  # Machine belongs to a person
    # new_individual_people.works_for.append(new_individual_organization)  # Person works for an organization

    new_individual_zone_rack.This_zone_rack_and_position_has_the_machine.append(new_individual_machine)
    new_individual_machine.This_machine_belongs_to_the_person.append(new_individual_people)

    new_individual_zone_rack.This_Rack_is_connectedto_this_PDU.append(new_individual_pdu)
    new_individual_pdu.This_PDU_is_connected_to_this_socket.append(new_individual_socket)
    new_individual_socket.This_socket_is_connected_to_this_MCB.append(new_individual_cmcb)
    new_individual_cmcb.This_MCB_is_connected_to_this_DB.append(new_individual_db)
    new_individual_db.This_Distribution_board_is_powered_by_this_UPS.append(new_individual_ups)
    new_individual_ups.This_UPS_is_being_backed_by_this_battery.append(new_individual_battery)



    

    # Add data properties
    # new_individual_rack.rack_no=(rack_no)
    # new_individual_rack.machine_no=machine_no

    # new_individual_machine.machine_model=machine_model
    # #new_individual_machine.machine_model.append(machine_model_name) for non functional 


    # new_individual_people.email.append(people_email)


    #rack and zone
    new_individual_zone_rack.rack_number.append(rack_number)
    new_individual_zone_rack.position.append(position_number)


    #machine
    new_individual_machine.cpu_model.append(cpu_model)
    new_individual_machine.cpu_frequency_MHZ.append(cpu_frequency_MHZ)
    new_individual_machine.date_install.append(date_install)
    new_individual_machine.host_name.append(host_name)
    new_individual_machine.machine_model.append(machine_model)
    new_individual_machine.memory_GB.append(memory_GB)
    new_individual_machine.network_port_open.append(network_port_open)
    new_individual_machine.power_watts.append(power_watts)
    new_individual_machine.pv4_address.append(ipv4_address)
    new_individual_machine.u_count.append(u_count)



    #people
    new_individual_people.department.append(department)
    new_individual_people.email.append(email)
    new_individual_people.phone_number.append(phone_number)
    new_individual_people.room_number.append(room_number)


    # Save the ontology
    onto.save(file="actual_owl_files/entended_protege.owl")
    print("Individual created and ontology saved successfully!")

    # Optionally run reasoner to infer properties
    with onto:
        sync_reasoner()




# Specify the current directory ('.') as the template folder
app = Flask(__name__)

@app.route('/')
def form():
    # Clear session at the start
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    form_data = decode_form_data(request.form)

    # Rack_instance = request.form['Rack_instance']#instance_name
    # rack_number = request.form['rack_number']
    # machine_number = request.form['machine_number']
    # Machine_instance=machine_number#instance_name
    # machine_model = request.form['machine_model']
    # People_instance = request.form['People_instance']#instance_name
    # people_email = request.form['People_email']
    # Organization_instance = request.form['Organization_instance']#instance_name


    zone_selection = request.form.get('zone_select').replace(' ', '_')
    rack_instance = request.form.get('Rack_instance').replace(' ', '_')
    rack_number = request.form.get('rack_number').replace(' ', '_')
    position_number = request.form.get('position_number').replace(' ', '_')
    
    machine_instance = request.form.get('machine_instance').replace(' ', '_')
    cpu_model = request.form.get('cpu_model').replace(' ', '_')
    cpu_frequency_MHZ = float(request.form.get('cpu_frequency_MHZ').replace(' ', '_'))
    date_install_str = request.form.get('date_install').replace(' ', '_')
    date_install = datetime.strptime(date_install_str, '%Y-%m-%d')
    host_name = request.form.get('host_name').replace(' ', '_')
    machine_model = request.form.get('machine_model').replace(' ', '_')
    memory_GB = float(request.form.get('memory_GB').replace(' ', '_'))
    network_port_open = int(request.form.get('network_port_open').replace(' ', '_'))
    power_watts = float(request.form.get('power_watts').replace(' ', '_'))
    ipv4_address = request.form.get('ipv4_address').replace(' ', '_')
    u_count = int(request.form.get('u_count').replace(' ', '_'))
    
    people_instance = request.form.get('People_instance').replace(' ', '_')
    department = request.form.get('department').replace(' ', '_')
    email = request.form.get('email').replace(' ', '_')
    phone_number = request.form.get('phone_number').replace(' ', '_')
    room_number = int(request.form.get('room_number').replace(' ', '_'))
    
    pdu_instance = request.form.get('pdu_instance').replace(' ', '_')
    
    socket_instance = request.form.get('socket_instance').replace(' ', '_')
    
    CMCB_instance = str(request.form.get('CMCB_instance').replace(' ', '_'))
    
    DB_instance = request.form.get('DB_instance').replace(' ', '_')
    
    UPS_instance = request.form.get('UPS_instance').replace(' ', '_')
    
    battery_instance = str(request.form.get('battery_instance').replace(' ', '_'))



    #create_ontology(Rack_instance, rack_number, machine_number, Machine_instance,machine_model, People_instance,people_email, Organization_instance)
    create_ontology(zone_selection, rack_instance, rack_number, position_number, machine_instance, cpu_model, cpu_frequency_MHZ, date_install, host_name, machine_model, memory_GB, network_port_open, power_watts, ipv4_address, u_count, people_instance, department, email, phone_number, room_number, pdu_instance, socket_instance, CMCB_instance, DB_instance, UPS_instance, battery_instance)

    #session.pop('zone_selection', None)
    #return redirect(url_for('form'))
    return f"Received data"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5001)