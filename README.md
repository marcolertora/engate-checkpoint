# enGate-checkpoint

## Reference
https://en.wikipedia.org/wiki/Finite-state_machine
https://en.wikipedia.org/wiki/UML_state_machine

## Breaking Changes
check_profile is replaced by check_zone
remove enroll from biometric device, now enroll is an autonomous system

## Stuff
ssh -R *:9999:127.0.0.1:9999 root@172.16.50.10

## Automaton

### link_config
i link_config se sono azioni:
    vengono passati alla fire del device
    (alla fire verrà passato anche edge_config)
se sono eventi
    vengono usati nella attach del event
    (nella trigger event verrà passato edge_config)

### node_config
i node_config descritti in automaton-->actions automaton-->states sono usati come config nei costruttori
di *State(node_id, config)* e *Action(node_id, config)*

TODO: nelle azioni potrebbero essere passati alla fire dei device e alla __call_ di user_tasks
TODO: negli eventi potrebbero essere passati alla attach event

### kwargs
i *kwarg*
1. partendo dalla *event.trigger*
2. passano alla *automaton.handle_event*
3a.. se process_event is false vengono messi in coda ù
4a..  quando verranno riesumati durante una *automaton.set_current_state* verrà richiamata la *automaton.handle_event* [2]
3. se process_event è true passano alla *state.handle_event* dello stato corrente
4. passano alla *node.next_node*
5. passano alla *node.enter* del prossimo nodo definito dall'edge che potrà essere *Action* o *State*
6a.. se *Action* viene passato nella call di tutti i task (user_tasks e device.fire)
7a.. nella user_tasks e nella device.fire vengono consumati i parametri (identifier nelle check*, per ora mai nelle fire)
8a.. passano alla action.handle_results
9a.. passano alla action.next_node e poi alla node.next_node [5] che continua il giro
6b.. se *State* viene passato alla "automaton.set_current_state"
7c.. nella set_current_state vengono consumati i parametri (initialized)
8d.. poi finisco interrompendo la chain

riassumendo i kwargs passati ad una event.trigger girano, attraverso le azioni che li useranno nella call dei tasks,
fino a che non atterrano su una set_current_state e poi vengono eliminati


### edge_config
gli edge config sono definiti nella descrizione dell'automaton e sono parametri che vengono usati nelle azioni
1. gli edge_config sono caricati negli automaton.edges
2. nella node.next_node vengono recuperati quelli dell'edge che si sta compiendo
3. passano alla *node.enter* del prossimo nodo definito dall'edge che potrà essere *Action* o *State*
4a.. se *Action* viene passato nella call di tutti i task (user_tasks e device.fire)
5a.. nella user_tasks e nella device.fire vengono consumati i parametri (status, direction.. nelle user_tasks, message...nelle fire)
6a.. poi finisco
4b.. se *State* viene passato alla "automaton.set_current_state"
5b.. poi finisco

### node_id e label
in automaton actions e states sono base_node_id e diventano i nodes_config
negli edge from e to sono full_node_id  vengono trasformati in base_node_id per essere legati ai nodes_config e
aggiunti ad automaton.nodes con il full_node_id
il throught ha label e se è vuoto di default è defaultchoices
nei namespace sono base_node_id




## TODO
[x] disabled config
[x] use pymodbus
[x] fix transit dict
[ ] replace xmlrpclib with twisted xmlrpc
[ ] downloader e uploader should share loop implementation
[x] auth logic should be moved to auth_provider
[x] exception when database is locked
[ ] check comment
[x] SERVER: fix people bound in offline sync object
[x] SERVER: add profile_zone in json offline sync object
[ ] generic usa of base object implementation (__init__, base, filename=modulename)
[ ] generic usa of slots
[ ] generic use of Enum
[ ] check lane repr and str, add direction and gate
[ ] expose lane in log
[ ] documentation 
[ ] replace copyright  in file
[ ] remove space between import and copyright

    def getLanesByProfileBadgePermissionId(tx, badgepermission_id, lane_id):
        """ retrive lanes allowed by profile from badgepermissions_id """

        query = '''SELECT l.lane_id
                   FROM bp_hostcompanyprofiles bphcp
                   JOIN hostcompanyprofiles_zones hcpz ON (hcpz.profile_id = bphcp.profile_id AND hcpz.company_id = bphcp.company_id)
                   JOIN zones_gates zg ON (zg.zone_id = hcpz.zone_id)
                   JOIN lanes l ON (l.gate_id = zg.gate_id AND zg.direction_id = l.direction_id)
                   WHERE bphcp.badgepermission_id = %s AND l.lane_id = %s''' % tx.sql(badgepermission_id, lane_id)

        return tx.select_all_dict(query)


#################################### verificato fino a qui

## Install

## Configuration

automaton_node_config automaton_edge_config e lane_device_config vengono accorpati e passati come parametri nella chiamata ai nodi

una lane_device puà avere node vuoto? non credo lo levo poi vediamo che succede

### Config

le config (lane_device_config) di del link lane device e node (lane_device) vengono mergiate con le config di automanode (automanode_config) e passate nella setevent al device nella link_device della lane

le config degli edge sono solo nella addEdge (forse)
le conf dei nodi sono usate nella costruzione dei nodi dell'automa


#
SITE
    GATE
        LANE



set_transit_status
actions --> transit --> lane --> message_encoder (per console)

set_transit_direction
actions --> transit --> lane --> message_encoder (per console)
oppure
device (piva, lr2000) --> transit --> lane --> message_encoder (per console)

reset_permission
actions --> transit --> lane --> message_encoder (per console)

add_premission
transit --> lane --> message_encoder (per console)

set_lane_status
actions --> lane --> message_encoder (per console)

start_transit
actions --> lane --> message_encoder (per console)

cleanLaneSpool
actions --> lane

add_attachment
transit --> lane
actions --> lane --> message_encoder (per console)

add_info
transit

### startup process
il main.py
# carica la configurazione dai file yaml con ruamel
# valida la configurazione con voluptuous
# avvia i servizi passando ad ognuno la sua porzione di conf
  . uploader
  . offlinesync
  . imager
  . checkpoint

le strutture dovrebbero essere:
self.items = dict(object_a_id=Object(a), object_b_id=Object(b),... )
le init degli oggetti dovrebbero essere __init__(self, object_id, config)
TODO: forse le conf vanno copiate

# checkpoint
nell __init_ del checkpoint vengono caricati dalla config:
 . default automaton nodes self.default_nodes
 . automaton self.automatons sono per struttura e helper per ora
 - lane_status in self.lane_status
 - lane_types in self.lane_types
 - security_level in self.security_levels
 . gate self.gates scorrendo tutti i sites
 . self.devices è inizializzato a dict() verra poi popolata del gate tramite la add_device
 . self.consoles  è inizializzato a dict() verra poi popolata del gate tramite la add_console

nella __init__ del gate
 . cerca tutti i device collegati alle sue lanes e per ogniuno chiama la add_device del checkpoint che lo istanzia
 e lo inserisce nei sui devices
 . cerca tutte le consoles collegate al gate e per ogniuna chiama la add_console del checkpoint che lo istanzia
 e la inserisce nelle sue consoles
 . inizializza tutte le lane in self.lanes tramite la self.add_lanes, la add_lane instanzia la lane aggiunge tutti i device collegati alla
 lanes e li linka, alla fine se gia presente nella self.lanes del gate lancia la detach della precedente e poi la sostituisce
 . avvia tutti gli automi delle sue lanes
 . avvia il loop che ricarica la configurazione ogni update_config_interval


nella lane
la direction è da conf e non puo cambiare
il type è da conf e non si può cambiare
lo status ha inizial state nella conf poi si può cambiare tramite action setLaneStatus nell'automaton
la security level è nel gate, puo cambiare tramite external  interface

l'automa viene scelto partendo dalla lane_type copn i seguenti valori (self.lane_status, self.security_level, self.direction)
quindi ad ofni cambio di questi valori deve essere ricontrollato e nel caso sostituito


gli stati e le azioni sono nodi del automa
la transazione da uno stato all'altro è definata da un edge che collega un nodo all'altro (from / to) tramite un evento throught

l'azione è di fatto uno stato dell'automa che  produce un output e passa immediatamente allo stato sucessivo .
l'output del nodo azione è in pratica l'evento usato come per scatenare la transazione allo stato successivo.
l'output del nodo azione è il risultato di un task eseguito (azione su un dispositivo , funzione ) nella enter-action dello stato trasformato in evento e utilizzato per triggerare l'immediata transazione al prossimo stato

gli eventi vendono iniettati nell'automa dai device
l'output di un azione può essere matchato per segliere un edge come se fosse un evento


            # from node and to node should be action or state
            # through_node should be event in a state starting edge or choice in action starting edge
            # choice could be none, event no.

## Usage

## Tools

## Authors


## TO CHANGE
#python and database
attachprefix=attach_prefix
listenport=listen_port
maxdelay=max_delay
privateKey=private_key
ridHoursTTL=num_of_hours
ports=units

#java and database
update-parkingslot=update-parking-slot
command_date=command_timestamp
lanelog_date=lanelog_timestamp


i transit aitem sono attaccati al transito e hanno allegati che vengono iviati insieme al transito
le plate ad esempio sono transit_items

gli identifier sono sono attaccati al transito
ma possono generare un permesso che potrà essere attaccato al transito
gli identifier (ex UID) sono identificatori "univoci" tipo badge,  barcode, etc.. che servono per risalire al permesso
la plate possono anche essere identifier oltre che transit_item ma sono un oggetto diverso
direi che quando c'e' una lettura targa la targa va inizialiizata sia come uid per l'auth sia come transit_item per la serializzazione

di base gli identifier fovrebbero essere usati solo per l'identificazione che dovrebbe sfociare un un permesso
non so se conviene serializzare anche quelli
i transit_item rimangono per tutto il transito possono essere usati a posteriori e verranno serializzati

quando un permesso identificato tramite un uid (badge) deve verificare le targhe associate al permesso con quelle lette usa la
plates_code di transit che scorre tutti i transit item e torna le plate code

transito sono attaccati
. permission che a loro volta contengono
. . identifier (uno solo) che a sua volta continiere:
. . . attachment? (forse non servono piu)
. . biometric
. attachments
. transit_item che a loro volta contiene:
. . attachments


ci sono alcuni device che triggerano eventi sul transito della fire come il camera/apnr/biometric
altri che triggerano su transito attualmente in corso sulal lane (reader)




## Installation
In order to install the enGate follow these steps:

+ Clone the the repository in the installation folder
  ```console
  cd /path/to/engate-checkpoint
  git clone http://git.infoporto.it/infoporto/engate-checkpoint .
  ```

+ Build and activate the python virtualenv and install the required packages
  ```console
  cd /path/to/engate-checkpoint
  virtualenv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

+ Create and customize the configuration files in the */etc/engate-checkpoint* folder
  **checkpoint.yaml** is the main one.
  ```console
     TODO: add a configuration example here
  ...
  ```

+ Configure the services to start on boot
  ```console
  systemctl edit --full --force engate-enroll
  ```

  Edit and customize the service's unit file
  ```
  [Unit]
  Description=enGate enroll
  After=network-online.target

  [Service]
  Type=simple
  StandardOutput=append:/var/log/engate-enroll.log
  StandardError=append:/var/log/engate-enroll.log
  ExecStart=/path/to/engate-checkpoint/venv/bin/python \
            /path/to/engate-checkpoint/checkpoint/enroll.py \
            --config-folder /etc/engate-checkpoint

  [Install]
  WantedBy=multi-user.target
  ```

  Enable the service and start it
  ```console
  systemctl --system daemon-reload
  systemctl enable engate-enroll
  systemctl start engate-enroll
  ```


+ Configure the services to start on boot
  ```console
  systemctl edit --full --force engate-checkpoint
  ```

  Edit and customize the service's unit file
  ```
  [Unit]
  Description=enGate checkpoint
  After=network-online.target

  [Service]
  Type=simple
  StandardOutput=append:/var/log/engate-checkpoint.log
  StandardError=append:/var/log/engate-checkpoint.log
  ExecStart=/path/to/engate-checkpoint/venv/bin/python \
            /path/to/engate-checkpoint/checkpoint/main.py \
            --config-folder /etc/engate-checkpoint

  [Install]
  WantedBy=multi-user.target
  ```

  Enable the service and start it
  ```console
  systemctl --system daemon-reload
  systemctl enable engate-checkpoint
  systemctl start engate-checkpoint
  ```

###
BADGE CODE:
6A006A7D35 Marco Lertora
trigger event VPR_BADGE identifier=6A006A7D35

070065A387 VF 000424
trigger event VPR_BADGE identifier=070065A387


##Translation
# build template (.pot)
xgettext -d checkpoint -o locales/checkpoint.pot device/devices/legacy/__init__.py main.py  authenticator/authenticator.py

# la prima volta
mkdir it/LC_MESSAGES
cp checkpoint.pot it/LC_MESSAGES/checkpoint.po
compile checkpoint.po
msgfmt locales/it/LC_MESSAGES/checkpoint.po -o locales/it/LC_MESSAGES/checkpoint.mo


# le altre volte
msgmerge --update locales/it/LC_MESSAGES/checkpoint.po locales/checkpoint.pot
