"""Manage the database and some other items required to run the API"""
from flask_script import Command, Manager, Option # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand, upgrade
from qsystem import db, application
from app import models
import logging

migrate = Migrate(application, db)
manager = Manager(application)

class Bootstrap(Command):

    def run(self):
        print("Clearing out all models")
        #models.Client.query.delete()
        #models.User.query.delete()
        models.Citizen.query.delete()
        models.CitizenState.query.delete()
        models.Channel.query.delete()
        models.Service.query.filter_by(actual_service_ind=1).delete()
        models.Service.query.delete()
        models.CSR.query.delete()
        models.CSRState.query.delete()
        models.Office.query.delete()
        models.SmartBoard.query.delete()
        models.Role.query.delete()
        db.session.commit()

        print("Starting to bootstrap data")

        smartboard1 = models.SmartBoard(sb_type="Test")

        db.session.add(smartboard1)
        db.session.flush()

        office1 = models.Office(
            office_name="Summerland", 
            office_number=1, 
            sb_id=smartboard1.sb_id
        )


        office2 = models.Office(
            office_name="Victoria", 
            office_number=2, 
            sb_id=smartboard1.sb_id
        )

        office3 = models.Office(
            office_name="Vernon", 
            office_number=3, 
            sb_id=smartboard1.sb_id
        )

        office4 = models.Office(
            office_name="Test Office", 
            office_number=4, 
            sb_id=smartboard1.sb_id
        )

        db.session.add(office1)
        db.session.add(office2)
        db.session.add(office3)
        db.session.add(office4)
        db.session.flush()

        category1 = models.Service(
            service_code = "abc123",
            service_name = "Licenses",
            service_desc = "Licenses - this is a description",
            #parent_id = 1,
            prefix = "L",
            display_dashboard_ind = 0,
            actual_service_ind = 0
        )

        category2 = models.Service(
            service_code = "abc1234",
            service_name = "Taxes",
            service_desc = "Taxes - this is a description",
            #parent_id = 2,
            prefix = "T",
            display_dashboard_ind = 0,
            actual_service_ind = 0
        )

        category3 = models.Service(
            service_code = "abc1235",
            service_name = "ICBC",
            service_desc = "ICBC - this is a description",
            #parent_id = 2,
            prefix = "I",
            display_dashboard_ind = 0,
            actual_service_ind = 0
        )

        db.session.add(category1)
        db.session.add(category2)
        db.session.add(category3)
        db.session.flush()

        service1 = models.Service(
            service_name = "Fishing",
            service_desc = "Fishing - this is a description",
            parent_id = category1.service_id,
            service_code = "abc1236",
            prefix = "F",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )

        service2 = models.Service(
            service_name = "Hunting",
            service_desc = "Hunting - this is a description",
            parent_id = category1.service_id,
            service_code = "abc1237",
            prefix = "H",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )

        service3 = models.Service(
            service_name = "Gold Mining",
            service_desc = "Gold Mining - this is a description",
            parent_id = category1.service_id,
            service_code = "abc1238",
            prefix = "G",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )

        service4 = models.Service(
            service_name = "Property Taxes",
            service_desc = "Property Taxes - this is a description",
            parent_id = category2.service_id,
            service_code = "abc1239",
            prefix = "P",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )

        service5 = models.Service(
            service_name = "MSP",
            service_desc = "MSP - this is a description",
            parent_id = category2.service_id,
            service_code = "abc12310",
            prefix = "M",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )

        service6 = models.Service(
            service_name = "Class 5 Test",
            service_desc = "Class 5 Test - this is a description",
            parent_id = category3.service_id,
            service_code = "abc12311",
            prefix = "C",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )

        service7 = models.Service(
            service_name = "Speeding Ticket",
            service_desc = "Speeding Ticket - this is a description",
            parent_id = category3.service_id,
            service_code = "abc12312",
            prefix = "S",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )

        service8 = models.Service(
            service_name = "Class 6 Test",
            service_desc = "Class 6 Test - this is a description",
            parent_id = category3.service_id,
            service_code = "abc12313",
            prefix = "C",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )

        service9 = models.Service(
            service_name = "DUI",
            service_desc = "DUI - this is a description",
            parent_id = category3.service_id,
            service_code = "abc12314",
            prefix = "D",
            display_dashboard_ind = 1,
            actual_service_ind = 1
        )

        db.session.add(service1)
        db.session.add(service2)
        db.session.add(service3)
        db.session.add(service4)
        db.session.add(service5)
        db.session.add(service6)
        db.session.add(service7)
        db.session.add(service8)
        db.session.add(service9)
        db.session.commit()

        office1.services.append(category1)
        office1.services.append(category2)
        office1.services.append(category3)
        office1.services.append(service1)
        office1.services.append(service2)
        office1.services.append(service3)
        office1.services.append(service4)
        office1.services.append(service5)
        office1.services.append(service6)
        office1.services.append(service7)
        office1.services.append(service8)
        office1.services.append(service9)

        office2.services.append(category2)
        office2.services.append(category3)
        office2.services.append(service4)
        office2.services.append(service5)
        office2.services.append(service6)
        office2.services.append(service7)
        office2.services.append(service8)
        office2.services.append(service9)

        office3.services.append(category1)
        office3.services.append(category2)
        office3.services.append(service1)
        office3.services.append(service2)
        office3.services.append(service3)
        office3.services.append(service4)
        office3.services.append(service5)

        office4.services.append(category1)
        office4.services.append(category2)
        office4.services.append(category3)
        office4.services.append(service1)
        office4.services.append(service2)
        office4.services.append(service3)
        office4.services.append(service4)
        office4.services.append(service5)
        office4.services.append(service6)
        office4.services.append(service7)
        office4.services.append(service8)
        office4.services.append(service9)

        role1 = models.Role(
            role_code="GA",
            role_desc="GA"
        )

        role2 = models.Role(
            role_code="CSR",
            role_desc="CSR"
        )

        db.session.add(role1)
        db.session.add(role2)
        db.session.commit()

        csr_state1 = models.CSRState(
            csr_state_name="Logout",
            csr_state_desc="Logging out"
        )

        csr_state2 = models.CSRState(
            csr_state_name="Login",
            csr_state_desc="Logging in"
        )

        csr_state3 = models.CSRState(
            csr_state_name="Break",
            csr_state_desc="Currently on break"
        )

        csr_state4 = models.CSRState(
            csr_state_name="Serving",
            csr_state_desc="Serving a citizen"
        )

        csr_state5 = models.CSRState(
            csr_state_name="Back Office",
            csr_state_desc="Currently in back office"
        )

        db.session.add(csr_state1)
        db.session.add(csr_state2)
        db.session.add(csr_state3)
        db.session.add(csr_state4)
        db.session.add(csr_state5)
        db.session.commit()


        adamkroon = models.CSR(
            username="adamkroon",  
            office_id=office1.office_id,
            role_id=role2.role_id,
            qt_xn_csr_ind=1,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state1.csr_state_id
            )

        cdmcinto = models.CSR(
            username="cdmcinto",
            office_id=office2.office_id,
            role_id=role1.role_id,
            qt_xn_csr_ind=1,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state2.csr_state_id
        )

        kgillani = models.CSR(
            username="kgillani",
            office_id=office1.office_id,
            role_id=role2.role_id,
            qt_xn_csr_ind=1,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state3.csr_state_id
        )

        scottrumsby = models.CSR(
            username="scottrumsby",
            office_id=office4.office_id,
            role_id= role1.role_id,
            qt_xn_csr_ind=1,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state4.csr_state_id
        )

        seanrumsby = models.CSR(
            username="seanrumsby",
            office_id=office3.office_id,
            role_id=role2.role_id,
            qt_xn_csr_ind=1,
            receptionist_ind=1,
            deleted=None,
            csr_state_id=csr_state5.csr_state_id
        )

        #cfms_postman_operator = models.User("cfms-postman-operator", office2.office_id)
        #cfms_postman_non_operator = models.User("cfms-postman-non-operator", office2.office_id)

        db.session.add(adamkroon)
        db.session.add(cdmcinto)
        db.session.add(kgillani)
        db.session.add(scottrumsby)
        db.session.add(seanrumsby)
        #db.session.add(cfms_postman_operator)
        #db.session.add(cfms_postman_non_operator)

        db.session.commit()

        cs1 = models.CitizenState(
            cs_state_name="Active",
            cs_state_desc="Citizen is active"
        )

        cs2 = models.CitizenState(
            cs_state_name="Received Services",
            cs_state_desc="Citizen has received services"
        )

        cs3 = models.CitizenState(
            cs_state_name="Left before receiving services",
            cs_state_desc="Citizen is now gone"
        )

        db.session.add(cs1)
        db.session.add(cs2)
        db.session.add(cs3)
        db.session.flush()

        john = models.Citizen(
            office_id = office1.office_id,
            ticket_number = "1",
            citizen_name = "John",
            citizen_comments = "Blorp",
            qt_xn_citizen_ind = 0,
            cs_id = cs1.cs_id,
            start_time  = '2018-06-23 10:22:30'
        )

        db.session.add(john)
        db.session.commit()

        channel1 = models.Channel(
            channel_name="In Person"
        )

        channel2 = models.Channel(
            channel_name="Telephone"
        )
        channel3 = models.Channel(
            channel_name="Email"
        )

        db.session.add(channel1)
        db.session.add(channel2)
        db.session.add(channel3)
        db.session.commit()

class FetchData(Command):

    def run(self):
        offices = db.session.query(models.Office).all()
        for o in offices:
            print(o.id, o.name)

class CreateUser(Command):
    option_list = (
        Option('--username', '-u', dest='username'),
        Option('--password', '-p', dest='password'),
        Option('--office_id', '-o', dest='office_id'),
    )

    def run(self, username, password, office_id):

        if username is None or password is None or office_id is None:
            exit("Error, username, password and office_id are all required")

        user = models.User(username, password, office_id)
        db.session.add(user)
        db.session.commit()

class MigrateWrapper(Command):
    def run(self):
        upgrade()

manager.add_command('db', MigrateCommand)
manager.add_command('migrate', MigrateWrapper())
manager.add_command('bootstrap', Bootstrap())
manager.add_command('fetch', FetchData())
manager.add_command('create_user', CreateUser())

if __name__ == '__main__':
    logging.log(logging.INFO, 'Running the Manager')
    manager.run()
