"""
This is the source code to a simple accounting app using Kivy GUI called EL-Count.
EL-count has been coded by the me https://github.com/TheMoonHashira on github.
The application can be used to manage a simple company.
The PieChart Module is from https://github.com/MrTequila/kivy-PieChart with some edits
"""

from kivymd.app import MDApp

from kivymd.uix.datatables import MDDataTable
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.togglebutton import ToggleButton

from kivy.metrics import dp
from kivy.core.window import Window

from Database.database import Employees, Clients, Services, Projects
from Modules.piechart import PieChart

Window.size = (1000, 600)
Window.minimum_width, Window.minimum_height = Window.size

# Saving some colors for further usage in piechart
colors = [
    [.9, .5, .1, 1],
    [.1, .9, .5, 1],
    [.5, .1, .9, 1],
    [.7, .4, .7, 1],
    [.8, .3, .6, 1],
    [.7, .2, .1, 1],
    [.7, .8, .9, 1],
    [.5, .4, .9, 1],
    [.2, .1, .9, 1],
    [.5, .1, .4, 1],
    [.3, .3, .3, 1],
    [.1, .5, .2, 1],
    [.5, .1, .5, 1],
    [.5, .5, .1, 1],
    [.9, .5, .5, 1],
    [.5, .9, .5, 1],
    [.1, .6, .9, 1],
    [.5, .5, .8, 1],
    [.9, .9, .1, 1],
    [.1, .7, .2, 1],
]


# define main page of the app
class MainPage(GridLayout):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.cols = 2
        self.padding = [0, 10, 0, 10]

        # Data for the Pie chart
        self.data = {'': (1, [0, 0, 0, 1])}
        self.refresh_chart(Button())
        position = (100, 0)
        size = (250, 250)
        self.chart = PieChart(data=self.data, position=position, size=size, legend_enable=True)
        # adding pie chart
        self.add_widget(self.chart)

        self.upper_right = GridLayout()
        self.upper_right.cols = 1
        self.upper_right.padding = [200, 100, 100, 100]
        self.add_widget(self.upper_right)

        # Add total_income division
        self.total_income = 0
        self.income_label = Label(text=f"Total Income:\n\n {self.total_income} IRR", font_size=30,
                                  color=(0, .8, .6, 1))
        self.refresh(Button())
        self.upper_right.add_widget(self.income_label)
        self.upper_right.add_widget(Label())
        button = Button(text='Refresh', font_size=20, on_release=self.refresh, color=(.5, .9, 1, 1))
        self.upper_right.add_widget(button)

        # Add company and accounting buttons to lead to their pages on click
        button = Button(text="Your Company", font_size=40, on_release=self.your_company_button, color=(.5, .9, 1, 1))
        self.add_widget(button)
        button = Button(text="Accounting", font_size=40, on_release=self.accounting_button, color=(.5, .9, 1, 1))
        self.add_widget(button)

    # Define referenced functions
    def refresh(self, instance):
        self.total_income = 0
        query = Projects.select(Projects.price)
        for price in query:
            self.total_income += price.price
        self.income_label.text = f"Total Income:\n\n {self.total_income} IRR"

    def refresh_chart(self, instance):
        services_query = Services.select()
        color_counter = 0
        values = []
        services_id = [service.id for service in services_query]
        services_name = [service.name for service in services_query]
        if services_name and services_id:
            for service_id in services_id:
                query = Projects.select(Projects.price).where(Projects.service_id == service_id)
                prices = [price.price for price in query]
                if prices:
                    values.append((sum(prices), colors[color_counter]))
                    color_counter += 1
                else:
                    services_id.remove(service_id)
                    services_name.remove(services_name[service_id - 1])
        if values:
            self.data = {}
            self.data = dict(zip(services_name, values))

    def your_company_button(self, instance):
        el_count.screen_manager.transition = SlideTransition(direction='right')
        el_count.screen_manager.current = "Company"

    def accounting_button(self, instance):
        el_count.screen_manager.transition = SlideTransition(direction='left')
        el_count.screen_manager.current = "Accounting"


# Define Accounting Page class
class AccountingPage(GridLayout):
    def __init__(self, **kwargs):
        super(AccountingPage, self).__init__(**kwargs)
        self.cols = 1

        self.upper = GridLayout()
        self.upper.cols = 2
        self.upper.row_force_default = True
        self.upper.row_default_height = 40
        self.upper.padding = [0, 0, 50, 0]
        self.add_widget(self.upper)

        # Adding back button
        button = Button(text="Go Back...", on_release=self.back_button, color=(0.5, .9, .5, 1), size_hint_x=None,
                        width=100)
        self.upper.add_widget(button)
        self.upper.add_widget(Label())

        self.upper.add_widget(Label())
        self.upper.add_widget(Label(text="Please fill the needed information below", color=(0.5, .9, .5, 1),
                                    size_hint_x=None, width=400))

        # Adding text inputs  with their labels
        label = Label(text='Project Name: ', font_size=20, color=(0.5, .9, .5, 1), size_hint_x=None, width=400)
        self.upper.add_widget(label)
        self.project_name = TextInput(multiline=False)
        self.upper.add_widget(self.project_name)

        label = Label(text='Service ID: ', font_size=20, color=(0.5, .9, .5, 1), size_hint_x=None, width=400)
        self.upper.add_widget(label)
        self.project_service = TextInput(multiline=False, input_filter='float')
        self.upper.add_widget(self.project_service)

        label = Label(text='Client ID: ', font_size=20, color=(0.5, .9, .5, 1), size_hint_x=None, width=400)
        self.upper.add_widget(label)
        self.project_client = TextInput(multiline=False, input_filter='float')
        self.upper.add_widget(self.project_client)

        label = Label(text='Paid price: ', font_size=20, color=(0.5, .9, .5, 1), size_hint_x=None, width=400)
        self.upper.add_widget(label)
        self.project_price = TextInput(multiline=False, input_filter='float')
        self.upper.add_widget(self.project_price)

        label = Label(text='Costs: ', font_size=20, color=(0.5, .9, .5, 1), size_hint_x=None, width=400)
        self.upper.add_widget(label)
        self.project_costs = TextInput(multiline=False, input_filter='float')
        self.upper.add_widget(self.project_costs)

        label = Label(text='Start Date: ', font_size=20, color=(0.5, .9, .5, 1), size_hint_x=None, width=400)
        self.upper.add_widget(label)
        self.project_start = TextInput(multiline=False, hint_text='ex: 2021-11-03')
        self.upper.add_widget(self.project_start)

        label = Label(text='Finished on: ', font_size=20, color=(0.5, .9, .5, 1), size_hint_x=None, width=400)
        self.upper.add_widget(label)
        self.project_end = TextInput(multiline=False, hint_text='ex: 2021-12-13')
        self.upper.add_widget(self.project_end)

        label = Label(text='Project Manager ID: ', font_size=20, color=(0.5, .9, .5, 1), size_hint_x=None, width=400)
        self.upper.add_widget(label)
        self.project_manager = TextInput(multiline=False, input_filter='float')
        self.upper.add_widget(self.project_manager)

        label = Label(text='Other accompanies: ', font_size=20, color=(0.5, .9, .5, 1), size_hint_x=None, width=400)
        self.upper.add_widget(label)
        self.project_accompanies = TextInput(multiline=False, hint_text='Employee ID separated by Dash - ex: 2-3-10 ')
        self.upper.add_widget(self.project_accompanies)

        label = Label(text='Your estimated Net profit is:', font_size=30, color=(1, .0, .5, 1))
        self.upper.add_widget(label)

        # Adding the output division
        self.output = Label(font_size=30, color=(1, .0, .5, 1))
        self.upper.add_widget(self.output)

        self.lower = GridLayout()
        self.add_widget(self.lower)
        self.lower.cols = 2
        self.lower.padding = [0, 200, 0, 0]

        # Calculate and save buttons
        button = Button(text='Calculate', font_size=30, on_release=self.calculate, color=(0.5, .9, .5, 1))
        self.lower.add_widget(button)

        button = Button(text='Save', font_size=30, on_release=self.open_popup, color=(0.5, .9, .5, 1))
        self.lower.add_widget(button)

        # Adding popup to make sure before saving the information
        popup = GridLayout()
        popup.cols = 1
        popup_buttons = GridLayout()
        popup_buttons.cols = 2

        label = Label(text='Are you sure you want to save this project?', font_size=20)
        popup.add_widget(label)

        button = Button(text='Cancel', on_release=self.close_popup, font_size=17)
        popup_buttons.add_widget(button)
        button = Button(text='Save', on_release=self.save_info, font_size=17)
        popup_buttons.add_widget(button)

        popup.add_widget(popup_buttons)
        self.save_popup = Popup(title='', content=popup, size_hint=(None, None), size=(600, 200))

    # Defining referenced functions
    def calculate(self, instance):
        try:
            net_profit = int(self.project_price.text) - int(self.project_costs.text)
        except:
            self.output.text = 'please fill the required parts'
        else:
            if net_profit < 0:
                self.output.text = f'{net_profit}'
            else:
                self.output.text = f'{net_profit}'

    def back_button(self, instance):
        el_count.screen_manager.transition = SlideTransition(direction='right')
        el_count.screen_manager.current = "Main"

    def save_info(self, instance):
        client_id = int(self.project_client.text)
        service_id = int(self.project_service.text)
        price = int(self.project_price.text)
        costs = int(self.project_costs.text)
        accompanies = self.project_accompanies.text.split('-') if self.project_accompanies.text else 0
        manager_id = int(self.project_manager.text)
        end_date = '0000-00-00' if not self.project_end.text else self.project_end.text

        Projects.insert(project_name=self.project_name.text, client_id=client_id,
                        service_id=service_id, price=price, costs=costs,
                        start_date=self.project_start.text, end_date=end_date,
                        manager_id=manager_id).execute()
        manager_cut = (price - costs) * 0.4
        Employees.update({Employees.savings: Employees.savings + manager_cut}).where(
            Employees.id == manager_id).execute()
        Employees.update({Employees.total_income: Employees.total_income + manager_cut}).where(
            Employees.id == manager_id).execute()

        if accompanies != 0:
            accompanies = [int(id) for id in accompanies]
            accompanies_cut = (price - (costs + manager_cut)) / len(accompanies)
            for emp_id in accompanies:
                Employees.update({Employees.savings: Employees.savings + accompanies_cut}).where(
                    Employees.id == emp_id).execute()
                Employees.update({Employees.total_income: Employees.total_income + accompanies_cut}).where(
                    Employees.id == emp_id).execute()

        self.project_name.text = self.project_client.text = self.project_service.text = self.project_price.text = ''
        self.project_costs.text = self.project_start.text = self.project_end.text = self.project_manager.text = ''
        self.project_accompanies.text = ''

        self.close_popup(instance)

    def open_popup(self, instance):
        if self.project_name.text and self.project_client.text and self.project_service.text and \
                self.project_price.text and self.project_costs.text and self.project_start.text and \
                self.project_end.text and self.project_manager.text:
            self.save_popup.open()
        else:
            self.output.text = 'please fill the required parts'

    def close_popup(self, instance):
        self.save_popup.dismiss()


# CompanyPage class to lead to data pages
class CompanyPage(GridLayout):
    def __init__(self, **kwargs):
        super(CompanyPage, self).__init__(**kwargs)
        self.cols = 1

        self.upper = GridLayout()
        self.upper.cols = 3
        self.upper.padding = [1, 1, 100, 100]
        self.add_widget(self.upper)

        # Go back button
        button = Button(text='Go Back...', font_size=20, on_release=self.go_back_button, color=(1, 1, 0, 1),
                        size_hint_x=None, width=100)
        self.upper.add_widget(button)
        self.upper.add_widget(Label(text='Access and edit data of your company. ', color=(1, 1, 0, 1), font_size=20))
        self.upper.add_widget(Label())

        self.upper.add_widget(Label())
        self.upper.add_widget(Label())
        self.upper.add_widget(Label())

        self.lower = GridLayout()
        self.lower.cols = 1
        self.lower.padding = [70, 1, 70, 70]
        self.add_widget(self.lower)

        # Referencing to different type of pages
        button = Button(text='Employees', font_size=20, color=(1, 1, 0, 1), on_release=self.go_employees_button)
        self.lower.add_widget(button)
        button = Button(text='Services', font_size=20, color=(1, 1, 0, 1), on_release=self.go_services_button)
        self.lower.add_widget(button)
        self.clients_button = Button(text='Clients', font_size=20, color=(1, 1, 0, 1),
                                     on_release=self.go_clients_button)
        self.lower.add_widget(self.clients_button)
        button = Button(text='Projects', font_size=20, color=(1, 1, 0, 1), on_release=self.go_projects_button)
        self.lower.add_widget(button)

    # Defining functions
    def go_back_button(self, instance):
        el_count.screen_manager.transition = SlideTransition(direction='left')
        el_count.screen_manager.current = "Main"

    def go_employees_button(self, instance):
        el_count.screen_manager.transition = SlideTransition(direction='right')
        el_count.screen_manager.current = "EmployeesPage"

    def go_services_button(self, instance):
        el_count.screen_manager.transition = SlideTransition(direction='right')
        el_count.screen_manager.current = "Services"

    def go_projects_button(self, instance):
        el_count.screen_manager.transition = SlideTransition(direction='right')
        el_count.screen_manager.current = "Projects"

    def go_clients_button(self, instance):
        el_count.screen_manager.transition = SlideTransition(direction='right')
        el_count.screen_manager.current = "Clients"


# Employee page for displaying and editing data
class EmployeesPage(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.upper = GridLayout()
        self.upper.cols = 5
        self.upper.row_force_default = True
        self.upper.row_default_height = 60
        self.add_widget(self.upper)

        button = Button(text='Go Back...', on_release=self.go_back_button)
        self.upper.add_widget(button)
        button = Button(text='Refresh', on_release=self.refresh)
        self.upper.add_widget(button)
        self.active_button = Button(text='All', on_release=self.active_filter)
        self.upper.add_widget(self.active_button)
        button = Button(text='Edit', on_release=self.open_edit_popup)
        self.upper.add_widget(button)
        button = Button(text='Add', on_release=self.open_popup)
        self.upper.add_widget(button)

        self.table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.9, 0.7),
            use_pagination=True,
            rows_num=10,
            pagination_menu_height='240dp',
            pagination_menu_pos="auto",
            background_color=[1, 0, 0, .5],

            column_data=[
                ('ID', dp(30)),
                ("First Name", dp(30)),
                ("Last Name", dp(30)),
                ("Birth Date", dp(30)),
                ('Phone Number', dp(30)),
                ('Email Address', dp(30)),
                ("Active", dp(30)),
                ('Total Income', dp(30)),
                ("Saving", dp(30))
            ],
            row_data=[]
        )
        self.add_widget(self.table)
        self.refresh(Button())

        # Add employee popup
        popup = GridLayout()
        popup.cols = 2
        button = Button(text='close', on_release=self.close_popup)
        popup.add_widget(button)
        label = Label(text='Fill the boxes below')
        popup.add_widget(label)

        label = Label(text='First Name:')
        popup.add_widget(label)
        self.employee_first_name = TextInput(multiline=False)
        popup.add_widget(self.employee_first_name)

        label = Label(text='Last Name:')
        popup.add_widget(label)
        self.employee_last_name = TextInput(multiline=False)
        popup.add_widget(self.employee_last_name)

        label = Label(text='Birth Date:')
        popup.add_widget(label)
        self.employee_birth_date = TextInput(hint_text='YYYY-MM-DD ex:2001-09-18', multiline=False)
        popup.add_widget(self.employee_birth_date)

        label = Label(text='Phone Number:')
        popup.add_widget(label)
        self.employee_phone_number = TextInput(input_filter='float', multiline=False)
        popup.add_widget(self.employee_phone_number)

        label = Label(text='Email:')
        popup.add_widget(label)
        self.employee_email = TextInput(multiline=False)
        popup.add_widget(self.employee_email)

        label = Label(text='Active:')
        popup.add_widget(label)
        toggle_layout = GridLayout()
        toggle_layout.cols = 2
        self.employee_btn_1 = ToggleButton(text='True', group='active', state='down')
        self.employee_btn_2 = ToggleButton(text='False', group='active')
        toggle_layout.add_widget(self.employee_btn_1)
        toggle_layout.add_widget(self.employee_btn_2)
        popup.add_widget(toggle_layout)
        self.employee_is_active = 'True' if self.employee_btn_1.state == 'down' else 'False'

        label = Label(text='Total Income:')
        popup.add_widget(label)
        self.employee_total_income = TextInput(input_filter='float', multiline=False)
        popup.add_widget(self.employee_total_income)

        label = Label(text='Savings:')
        popup.add_widget(label)
        self.employee_savings = TextInput(input_filter='float', multiline=False)
        popup.add_widget(self.employee_savings)

        popup.add_widget(Label())
        button = Button(text='SAVE', on_release=self.open_check_popup)
        popup.add_widget(button)

        self.add_popup = Popup(title='Add employee', content=popup, size_hint=(None, None), size=(500, 500),
                               title_align='center')

        # Add popup to make sure before adding
        popup = GridLayout()
        popup.cols = 1
        popup_buttons = GridLayout()
        popup_buttons.cols = 2

        label = Label(text='Are you sure you want to add this employee?', font_size=20)
        popup.add_widget(label)

        button = Button(text='Cancel', on_release=self.close_check_popup, font_size=17)
        popup_buttons.add_widget(button)
        button = Button(text='Add', on_release=self.save_info, font_size=17)
        popup_buttons.add_widget(button)

        popup.add_widget(popup_buttons)
        self.check_popup = Popup(title='', content=popup, size_hint=(None, None), size=(600, 200))

        # Add popup to edit data
        popup = GridLayout()
        popup.cols = 2
        button = Button(text="Close", on_release=self.close_edit_popup)
        popup.add_widget(button)
        self.edit_label = Label()
        popup.add_widget(self.edit_label)

        label = Label(text='Type the ID you want to edit or delete:')
        popup.add_widget(label)
        self.edit_ID = TextInput(multiline=False, hint_text='Type ALL to delete all the data')
        popup.add_widget(self.edit_ID)

        button = Button(text='Delete', on_release=self.open_delete_popup)
        popup.add_widget(button)
        button = Button(text='Edit', on_release=self.open_edit_page)
        popup.add_widget(button)

        self.edit_popup = Popup(title='Edit', content=popup, size_hint=(None, None), size=(600, 200),
                                title_align='center')

        # Add delete popup
        popup = GridLayout()
        popup.cols = 1
        popup_lower = GridLayout()
        popup_lower.cols = 2

        self.delete_popup_label = Label(text='Are you sure you want to delete the selected IDs?')
        popup.add_widget(self.delete_popup_label)

        button = Button(text='Cancel', on_release=self.close_delete_popup)
        popup_lower.add_widget(button)

        button = Button(text='Delete', on_release=self.delete_employees)
        popup_lower.add_widget(button)

        popup.add_widget(popup_lower)

        self.delete_popup = Popup(title='', content=popup, size_hint=(None, None), size=(600, 200))

        # Add edit popup
        popup = GridLayout()
        popup.cols = 2
        button = Button(text='close', on_release=self.close_edit_page)
        popup.add_widget(button)
        label = Label(text='Edit the data below')
        popup.add_widget(label)

        label = Label(text='First Name:')
        popup.add_widget(label)
        self.edit_employee_first_name = TextInput(multiline=False)
        popup.add_widget(self.edit_employee_first_name)

        label = Label(text='Last Name:')
        popup.add_widget(label)
        self.edit_employee_last_name = TextInput(multiline=False)
        popup.add_widget(self.edit_employee_last_name)

        label = Label(text='Birth Date:')
        popup.add_widget(label)
        self.edit_employee_birth_date = TextInput(multiline=False)
        popup.add_widget(self.edit_employee_birth_date)

        label = Label(text='Phone Number:')
        popup.add_widget(label)
        self.edit_employee_phone_number = TextInput(multiline=False)
        popup.add_widget(self.edit_employee_phone_number)

        label = Label(text='Email:')
        popup.add_widget(label)
        self.edit_employee_email = TextInput(multiline=False)
        popup.add_widget(self.edit_employee_email)

        label = Label(text='Active:')
        popup.add_widget(label)
        toggle_layout = GridLayout()
        toggle_layout.cols = 2
        self.btn_1 = ToggleButton(text='True', group='active')
        self.btn_2 = ToggleButton(text='False', group='active')
        toggle_layout.add_widget(self.btn_1)
        toggle_layout.add_widget(self.btn_2)
        popup.add_widget(toggle_layout)
        self.edit_employee_is_active = 'True' if self.btn_1.state == 'down' else 'False'

        label = Label(text='Total Income:')
        popup.add_widget(label)
        self.edit_employee_total_income = TextInput(multiline=False)
        popup.add_widget(self.edit_employee_total_income)

        label = Label(text='Savings:')
        popup.add_widget(label)
        self.edit_employee_savings = TextInput(multiline=False)
        popup.add_widget(self.edit_employee_savings)

        popup.add_widget(Label())
        button = Button(text='SAVE', on_release=self.open_check_page)
        popup.add_widget(button)

        self.edit_page = Popup(title='Edit employee', content=popup, size_hint=(None, None), size=(500, 500),
                               title_align='center')

        # Check popup
        popup = GridLayout()
        popup.cols = 1
        popup_buttons = GridLayout()
        popup_buttons.cols = 2

        label = Label(text='Are you sure you want to edit this employee?', font_size=20)
        popup.add_widget(label)
        button = Button(text='Cancel', on_release=self.close_check_page, font_size=17)
        popup_buttons.add_widget(button)
        button = Button(text='Edit', on_release=self.edit_info, font_size=17)
        popup_buttons.add_widget(button)

        popup.add_widget(popup_buttons)
        self.check_page = Popup(title='', content=popup, size_hint=(None, None), size=(600, 200))

    def active_filter(self, instance):
        if self.active_button.text == 'Active':
            self.active_button.text = 'Inactive'
        elif self.active_button.text == 'Inactive':
            self.active_button.text = 'All'
        else:
            self.active_button.text = 'Active'
        self.refresh(instance)

    def open_check_page(self, instance):
        if self.edit_employee_first_name.text and self.edit_employee_last_name.text and \
                self.edit_employee_birth_date.text and self.edit_employee_phone_number.text and \
                self.edit_employee_email.text and self.edit_employee_is_active and self.edit_employee_savings.text and \
                self.edit_employee_total_income.text:
            self.check_page.open()

    def close_check_page(self, instance):
        self.check_page.dismiss(instance)

    def edit_info(self, instance):
        try:
            self.edit_employee_is_active = 'True' if self.btn_1.state == 'down' else 'False'
            Employees.update({Employees.first_name: self.edit_employee_first_name.text,
                              Employees.last_name: self.edit_employee_last_name.text,
                              Employees.birth_date: self.edit_employee_birth_date.text,
                              Employees.phone_number: int(self.edit_employee_phone_number.text),
                              Employees.email_address: self.edit_employee_email.text,
                              Employees.is_active: self.edit_employee_is_active,
                              Employees.total_income: int(self.edit_employee_total_income.text),
                              Employees.savings: int(self.edit_employee_savings.text)}).where(
                Employees.id == int(self.edit_ID.text)).execute()
        except:
            self.close_check_page(instance)
        else:
            self.close_check_page(instance)
            self.close_edit_page(instance)
            self.close_edit_popup(instance)
            self.refresh(instance)

    def delete_employees(self, instance):
        try:
            if self.edit_ID.text != 'ALL':
                to_delete = self.edit_ID.text.split('-')
                to_delete = [int(i) for i in to_delete]
                for candidate in to_delete:
                    Employees.delete().where(Employees.id == candidate).execute()
                self.close_delete_popup(instance)
                self.close_edit_popup(instance)
            elif self.edit_ID.text == 'ALL':
                query = Employees.select(Employees.id)
                for employee in query:
                    Employees.delete().where(Employees.id == employee).execute()
            else:
                self.delete_popup_label.text = 'Check the input again'

            self.refresh(instance)
            self.close_delete_popup(instance)
            self.close_edit_popup(instance)
        except:
            pass

    def open_delete_popup(self, instance):
        if self.edit_ID.text:
            self.delete_popup.open()
        else:
            self.edit_label.text = 'Please fill the box'

    def close_delete_popup(self, instance):
        self.delete_popup.dismiss()

    def open_edit_page(self, instance):
        try:
            to_edit = int(self.edit_ID.text)
        except:
            self.edit_label.text = 'Please fill the box'
        else:
            try:
                if self.edit_ID.text:
                    query = Employees.select().where(Employees.id == int(self.edit_ID.text))
                    self.edit_employee_first_name.text = query[0].first_name
                    self.edit_employee_last_name.text = query[0].last_name
                    birth_date = str(query[0].birth_date)
                    self.edit_employee_birth_date.text = birth_date
                    self.edit_employee_phone_number.text = str(query[0].phone_number)
                    self.edit_employee_email.text = query[0].email_address
                    if query[0].is_active == 'True':
                        self.btn_1.state = 'down'
                    else:
                        self.btn_2.state = 'down'
                    self.edit_employee_total_income.text = str(query[0].total_income)
                    self.edit_employee_savings.text = str(query[0].savings)
                    self.edit_page.open()
                else:
                    self.edit_label.text = 'Please fill the box'
            except:
                self.edit_label.text = 'Fill the box with available IDs'

    def close_edit_page(self, instance):
        self.edit_page.dismiss()

    def go_back_button(self, instance):
        el_count.screen_manager.transition = SlideTransition(direction='left')
        el_count.screen_manager.current = "Company"

    def open_popup(self, instance):
        self.add_popup.open()

    def close_popup(self, instance):
        self.add_popup.dismiss()

    def open_edit_popup(self, instance):
        self.edit_popup.open()

    def close_edit_popup(self, instance):
        self.edit_popup.dismiss()

    def save_info(self, instance):
        try:
            self.employee_is_active = 'True' if self.employee_btn_1.state == 'down' else 'False'
            phone_number = int(self.employee_phone_number.text)
            total_income = int(self.employee_total_income.text)
            savings = int(self.employee_savings.text)

            Employees.insert(first_name=self.employee_first_name.text, last_name=self.employee_last_name.text,
                             birth_date=self.employee_birth_date.text, phone_number=phone_number,
                             email_address=self.employee_email.text, is_active=self.employee_is_active,
                             total_income=total_income, savings=savings).execute()
            self.employee_first_name.text = self.employee_last_name.text = self.employee_birth_date.text = \
                self.employee_phone_number.text = self.employee_email.text = self.employee_is_active.text = \
                self.employee_savings.text = self.employee_total_income.text = ''
        except:
            self.close_check_popup(instance)
            self.close_popup(instance)
            self.refresh(instance)
        else:
            self.close_check_popup(instance)
            self.close_popup(instance)
            self.refresh(instance)

    def open_check_popup(self, instance):
        if self.employee_first_name.text and self.employee_last_name.text and self.employee_birth_date.text and \
                self.employee_phone_number.text and self.employee_email.text and self.employee_is_active and \
                self.employee_total_income.text and self.employee_savings.text:
            self.check_popup.open()

    def close_check_popup(self, instance):
        self.check_popup.dismiss()

    def refresh(self, instance):
        if self.active_button.text == 'Active':
            query = Employees.select().where(Employees.is_active == 'True')
        elif self.active_button.text == 'Inactive':
            query = Employees.select().where(Employees.is_active == 'False')
        else:
            query = Employees.select()
        all_tuples = []
        for employee in query:
            temp = (employee.id, employee.first_name, employee.last_name, employee.birth_date, employee.phone_number,
                    employee.email_address, employee.is_active, employee.total_income, employee.savings)
            all_tuples.append(temp)
        if len(all_tuples) == 1:
            all_tuples.insert(0, ('', '', '', '', '', '', '', '', ''))
        self.table.row_data = all_tuples


# Service page for displaying and editing data
class ServicesPage(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.upper = GridLayout()
        self.upper.cols = 4
        self.upper.row_force_default = True
        self.upper.row_default_height = 60
        self.add_widget(self.upper)

        button = Button(text='Go Back...', on_release=self.go_back_button)
        self.upper.add_widget(button)
        button = Button(text='Refresh', on_release=self.refresh)
        self.upper.add_widget(button)
        button = Button(text='Edit', on_release=self.open_edit_popup)
        self.upper.add_widget(button)
        button = Button(text='Add', on_release=self.open_popup)
        self.upper.add_widget(button)

        self.table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.9, 0.7),
            use_pagination=True,
            rows_num=10,
            pagination_menu_height='240dp',
            pagination_menu_pos="auto",
            background_color=[1, 0, 0, .5],

            column_data=[
                ("ID", dp(30)),
                ("Service Name", dp(30)),
                ("Service Info", dp(30))
            ],
            row_data=[]
        )
        self.add_widget(self.table)
        self.refresh(Button())

        popup = GridLayout()
        popup.cols = 2
        button = Button(text='close', on_release=self.close_popup)
        popup.add_widget(button)
        label = Label(text='Fill the boxes below')
        popup.add_widget(label)

        label = Label(text='Service Name:')
        popup.add_widget(label)
        self.service_name = TextInput(multiline=False)
        popup.add_widget(self.service_name)

        label = Label(text='Information:')
        popup.add_widget(label)
        self.service_info = TextInput()
        popup.add_widget(self.service_info)

        popup.add_widget(Label())
        button = Button(text='SAVE', on_release=self.open_check_popup)
        popup.add_widget(button)

        self.add_popup = Popup(title='Add service', content=popup, size_hint=(None, None), size=(500, 500),
                               title_align='center')

        # Add popup to make sure before adding
        popup = GridLayout()
        popup.cols = 1
        popup_buttons = GridLayout()
        popup_buttons.cols = 2

        label = Label(text='Are you sure you want to add this service?', font_size=20)
        popup.add_widget(label)

        button = Button(text='Cancel', on_release=self.close_check_popup, font_size=17)
        popup_buttons.add_widget(button)
        button = Button(text='Add', on_release=self.save_info, font_size=17)
        popup_buttons.add_widget(button)

        popup.add_widget(popup_buttons)
        self.check_popup = Popup(title='', content=popup, size_hint=(None, None), size=(600, 200))

        # Add edit popup
        popup = GridLayout()
        popup.cols = 2
        button = Button(text="Close", on_release=self.close_edit_popup)
        popup.add_widget(button)
        self.edit_label = Label()
        popup.add_widget(self.edit_label)

        label = Label(text='Type the ID you want to edit or delete:')
        popup.add_widget(label)
        self.edit_ID = TextInput(multiline=False, hint_text='Type ALL to delete all the data')
        popup.add_widget(self.edit_ID)

        button = Button(text='Delete', on_release=self.open_delete_popup)
        popup.add_widget(button)
        button = Button(text='Edit', on_release=self.open_edit_page)
        popup.add_widget(button)

        self.edit_popup = Popup(title='Edit', content=popup, size_hint=(None, None), size=(600, 200),
                                title_align='center')

        # Add delete popup
        popup = GridLayout()
        popup.cols = 1
        popup_lower = GridLayout()
        popup_lower.cols = 2

        self.delete_popup_label = Label(text='Are you sure you want to delete the selected IDs?')
        popup.add_widget(self.delete_popup_label)

        button = Button(text='Cancel', on_release=self.close_delete_popup)
        popup_lower.add_widget(button)

        button = Button(text='Delete', on_release=self.delete_service)
        popup_lower.add_widget(button)

        popup.add_widget(popup_lower)

        self.delete_popup = Popup(title='', content=popup, size_hint=(None, None), size=(600, 200))

        # Add edit page
        popup = GridLayout()
        popup.cols = 2
        button = Button(text='close', on_release=self.close_edit_page)
        popup.add_widget(button)
        label = Label(text='Edit the data below')
        popup.add_widget(label)

        label = Label(text='Service Name:')
        popup.add_widget(label)
        self.edit_service_name = TextInput(multiline=False)
        popup.add_widget(self.edit_service_name)

        label = Label(text='Service Information:')
        popup.add_widget(label)
        self.edit_service_info = TextInput(multiline=False)
        popup.add_widget(self.edit_service_info)

        popup.add_widget(Label())
        button = Button(text='SAVE', on_release=self.open_check_page)
        popup.add_widget(button)

        self.edit_page = Popup(title='Edit service', content=popup, size_hint=(None, None), size=(500, 500),
                               title_align='center')

        # Check popup
        popup = GridLayout()
        popup.cols = 1
        popup_buttons = GridLayout()
        popup_buttons.cols = 2

        label = Label(text='Are you sure you want to edit this service?', font_size=20)
        popup.add_widget(label)
        button = Button(text='Cancel', on_release=self.close_check_page, font_size=17)
        popup_buttons.add_widget(button)
        button = Button(text='Edit', on_release=self.edit_info, font_size=17)
        popup_buttons.add_widget(button)

        popup.add_widget(popup_buttons)
        self.check_page = Popup(title='', content=popup, size_hint=(None, None), size=(600, 200))

    def open_check_page(self, instance):
        if self.edit_service_name.text and self.edit_service_info.text:
            self.check_page.open()

    def close_check_page(self, instance):
        self.check_page.dismiss(instance)

    def edit_info(self, instance):
        try:
            Services.update({Services.name: self.edit_service_name.text,
                             Services.info: self.edit_service_info.text}).where(
                Services.id == int(self.edit_ID.text)).execute()
        except:
            self.close_check_page(instance)
        else:
            self.close_check_page(instance)
            self.close_edit_page(instance)
            self.close_edit_popup(instance)
            self.refresh(instance)

    def delete_service(self, instance):
        try:
            if self.edit_ID.text != 'ALL':
                to_delete = self.edit_ID.text.split('-')
                to_delete = [int(i) for i in to_delete]
                for candidate in to_delete:
                    Services.delete().where(Services.id == candidate).execute()
                self.close_delete_popup(instance)
                self.close_edit_popup(instance)
            elif self.edit_ID.text == 'ALL':
                query = Services.select(Employees.id)
                for service in query:
                    Services.delete().where(Services.id == service).execute()
            else:
                self.delete_popup_label.text = 'Check the input again'

            self.refresh(instance)
            self.close_delete_popup(instance)
            self.close_edit_popup(instance)
        except:
            pass

    def open_delete_popup(self, instance):
        if self.edit_ID.text:
            self.delete_popup.open()
        else:
            self.edit_label.text = 'Please fill the box'

    def close_delete_popup(self, instance):
        self.delete_popup.dismiss()

    def open_edit_page(self, instance):
        try:
            to_edit = int(self.edit_ID.text)
        except:
            self.edit_label.text = 'Please fill the box'
        else:
            try:
                if self.edit_ID.text:
                    query = Services.select().where(Services.id == int(self.edit_ID.text))
                    self.edit_service_name.text = query[0].name
                    self.edit_service_info.text = query[0].info
                    self.edit_page.open()
                else:
                    self.edit_label.text = 'Please fill the box'
            except:
                self.edit_label.text = 'Fill the box with available IDs'

    def close_edit_page(self, instance):
        self.edit_page.dismiss()

    def open_edit_popup(self, instance):
        self.edit_popup.open()

    def close_edit_popup(self, instance):
        self.edit_popup.dismiss()

    def go_back_button(self, instance):
        el_count.screen_manager.transition = SlideTransition(direction='left')
        el_count.screen_manager.current = "Company"

    def open_popup(self, instance):
        self.add_popup.open()

    def close_popup(self, instance):
        self.add_popup.dismiss()

    def save_info(self, instance):
        try:
            Services.insert(name=self.service_name.text, info=self.service_info.text).execute()
            self.service_name.text = self.service_info.text = ''
        except:
            self.close_check_popup(instance)
            self.close_popup(instance)
            self.refresh(instance)
        else:
            self.close_check_popup(instance)
            self.close_popup(instance)
            self.refresh(instance)

    def open_check_popup(self, instance):
        self.check_popup.open()

    def close_check_popup(self, instance):
        self.check_popup.dismiss()

    def refresh(self, instance):
        query = Services.select().order_by(Services.id)
        all_tuples = []
        for service in query:
            temp = (service.id, service.name, service.info)
            all_tuples.append(temp)
        if len(all_tuples) == 1:
            all_tuples.insert(0, ('', '', ''))
        self.table.row_data = all_tuples


# Client page for displaying and editing data
class ClientsPage(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.upper = GridLayout()
        self.upper.cols = 4
        self.upper.row_force_default = True
        self.upper.row_default_height = 60
        self.add_widget(self.upper)

        button = Button(text='Go Back...', on_release=self.go_back_button)
        self.upper.add_widget(button)
        button = Button(text='Refresh', on_release=self.refresh)
        self.upper.add_widget(button)
        button = Button(text='Edit', on_release=self.open_edit_popup)
        self.upper.add_widget(button)
        button = Button(text='Add', on_release=self.open_popup)
        self.upper.add_widget(button)

        self.table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(1, 0.7),
            use_pagination=True,
            rows_num=10,
            pagination_menu_height='240dp',
            pagination_menu_pos="auto",
            background_color=[1, 0, 0, .5],

            column_data=[
                ("ID", dp(30)),
                ("Client Name", dp(30)),
                ("Client Surname", dp(30)),
                ("Phone Number", dp(30)),
                ("Email", dp(30)),
                ('Address', dp(30))
            ],
            row_data=[]
        )
        self.add_widget(self.table)
        self.refresh(Button())

        popup = GridLayout()
        popup.cols = 2
        button = Button(text='close', on_release=self.close_popup)
        popup.add_widget(button)
        label = Label(text='Fill the boxes below')
        popup.add_widget(label)

        label = Label(text='First Name:')
        popup.add_widget(label)
        self.client_first_name = TextInput(multiline=False)
        popup.add_widget(self.client_first_name)

        label = Label(text='Last Name:')
        popup.add_widget(label)
        self.client_last_name = TextInput(multiline=False)
        popup.add_widget(self.client_last_name)

        label = Label(text='Phone Number:')
        popup.add_widget(label)
        self.client_phone_number = TextInput(input_filter='float', multiline=False)
        popup.add_widget(self.client_phone_number)

        label = Label(text='Email Address:')
        popup.add_widget(label)
        self.client_email = TextInput(multiline=False)
        popup.add_widget(self.client_email)

        label = Label(text='Address:')
        popup.add_widget(label)
        self.client_address = TextInput()
        popup.add_widget(self.client_address)

        popup.add_widget(Label())
        button = Button(text='SAVE', on_release=self.open_check_popup)
        popup.add_widget(button)

        self.add_popup = Popup(title='Add client', content=popup, size_hint=(None, None), size=(500, 500),
                               title_align='center')

        # Add popup to make sure before adding
        popup = GridLayout()
        popup.cols = 1
        popup_buttons = GridLayout()
        popup_buttons.cols = 2

        label = Label(text='Are you sure you want to add this client?', font_size=20)
        popup.add_widget(label)

        button = Button(text='Cancel', on_release=self.close_check_popup, font_size=17)
        popup_buttons.add_widget(button)
        button = Button(text='Add', on_release=self.save_info, font_size=17)
        popup_buttons.add_widget(button)

        popup.add_widget(popup_buttons)
        self.check_popup = Popup(title='', content=popup, size_hint=(None, None), size=(600, 200))

        # Add popup to edit data
        popup = GridLayout()
        popup.cols = 2
        button = Button(text="Close", on_release=self.close_edit_popup)
        popup.add_widget(button)
        self.edit_label = Label()
        popup.add_widget(self.edit_label)

        label = Label(text='Type the ID you want to edit or delete:')
        popup.add_widget(label)
        self.edit_ID = TextInput(multiline=False, hint_text='Type ALL to delete all the data')
        popup.add_widget(self.edit_ID)

        button = Button(text='Delete', on_release=self.open_delete_popup)
        popup.add_widget(button)
        button = Button(text='Edit', on_release=self.open_edit_page)
        popup.add_widget(button)

        self.edit_popup = Popup(title='Edit', content=popup, size_hint=(None, None), size=(600, 200),
                                title_align='center')

        # Add delete popup
        popup = GridLayout()
        popup.cols = 1
        popup_lower = GridLayout()
        popup_lower.cols = 2

        self.delete_popup_label = Label(text='Are you sure you want to delete the selected IDs?')
        popup.add_widget(self.delete_popup_label)

        button = Button(text='Cancel', on_release=self.close_delete_popup)
        popup_lower.add_widget(button)

        button = Button(text='Delete', on_release=self.delete_clients)
        popup_lower.add_widget(button)

        popup.add_widget(popup_lower)

        self.delete_popup = Popup(title='', content=popup, size_hint=(None, None), size=(600, 200))

        # Add edit popup
        popup = GridLayout()
        popup.cols = 2
        button = Button(text='close', on_release=self.close_edit_page)
        popup.add_widget(button)
        label = Label(text='Edit the data below')
        popup.add_widget(label)

        label = Label(text='First Name:')
        popup.add_widget(label)
        self.edit_client_first_name = TextInput(multiline=False)
        popup.add_widget(self.edit_client_first_name)

        label = Label(text='Last Name:')
        popup.add_widget(label)
        self.edit_client_last_name = TextInput(multiline=False)
        popup.add_widget(self.edit_client_last_name)

        label = Label(text='Phone Number:')
        popup.add_widget(label)
        self.edit_client_phone_number = TextInput(multiline=False)
        popup.add_widget(self.edit_client_phone_number)

        label = Label(text='Email Address:')
        popup.add_widget(label)
        self.edit_client_email = TextInput(multiline=False)
        popup.add_widget(self.edit_client_email)

        label = Label(text='Address:')
        popup.add_widget(label)
        self.edit_client_address = TextInput(multiline=False)
        popup.add_widget(self.edit_client_address)

        popup.add_widget(Label())
        button = Button(text='SAVE', on_release=self.open_check_page)
        popup.add_widget(button)

        self.edit_page = Popup(title='Edit client', content=popup, size_hint=(None, None), size=(500, 500),
                               title_align='center')

        # Check popup
        popup = GridLayout()
        popup.cols = 1
        popup_buttons = GridLayout()
        popup_buttons.cols = 2

        label = Label(text='Are you sure you want to edit this client?', font_size=20)
        popup.add_widget(label)
        button = Button(text='Cancel', on_release=self.close_check_page, font_size=17)
        popup_buttons.add_widget(button)
        button = Button(text='Edit', on_release=self.edit_info, font_size=17)
        popup_buttons.add_widget(button)

        popup.add_widget(popup_buttons)
        self.check_page = Popup(title='', content=popup, size_hint=(None, None), size=(600, 200))

    def open_check_page(self, instance):
        if self.edit_client_first_name.text and self.edit_client_last_name.text and self.edit_client_phone_number and \
                self.edit_client_email.text and self.edit_client_address.text:
            self.check_page.open()

    def close_check_page(self, instance):
        self.check_page.dismiss(instance)

    def edit_info(self, instance):
        try:
            Clients.update({Clients.first_name: self.edit_client_first_name.text,
                            Clients.last_name: self.edit_client_last_name.text,
                            Clients.phone: int(self.edit_client_phone_number.text),
                            Clients.email: self.edit_client_email.text,
                            Clients.address: self.edit_client_address.text}).where(
                Clients.id == int(self.edit_ID.text)).execute()
        except:
            self.close_check_page(instance)
        else:
            self.close_check_page(instance)
            self.close_edit_page(instance)
            self.close_edit_popup(instance)
            self.refresh(instance)

    def delete_clients(self, instance):
        try:
            if self.edit_ID.text != 'ALL':
                to_delete = self.edit_ID.text.split('-')
                to_delete = [int(i) for i in to_delete]
                for candidate in to_delete:
                    Clients.delete().where(Clients.id == candidate).execute()
                self.close_delete_popup(instance)
                self.close_edit_popup(instance)
            elif self.edit_ID.text == 'ALL':
                query = Clients.select(Clients.id)
                for client in query:
                    Clients.delete().where(Clients.id == client).execute()
            else:
                self.delete_popup_label.text = 'Check the input again'

            self.refresh(instance)
            self.close_delete_popup(instance)
            self.close_edit_popup(instance)
        except:
            pass

    def open_delete_popup(self, instance):
        if self.edit_ID.text:
            self.delete_popup.open()
        else:
            self.edit_label.text = 'Please fill the box'

    def close_delete_popup(self, instance):
        self.delete_popup.dismiss()

    def open_edit_page(self, instance):
        try:
            to_edit = int(self.edit_ID.text)
        except:
            self.edit_label.text = 'Please fill the box'
        else:
            try:
                if self.edit_ID.text:
                    query = Clients.select().where(Clients.id == int(self.edit_ID.text))
                    self.edit_client_first_name.text = query[0].first_name
                    self.edit_client_last_name.text = query[0].last_name
                    self.edit_client_phone_number.text = str(query[0].phone)
                    self.edit_client_email.text = query[0].email
                    self.edit_client_address.text = query[0].address
                    self.edit_page.open()
                else:
                    self.edit_label.text = 'Please fill the box'
            except:
                self.edit_label.text = 'Fill the box with available IDs'

    def close_edit_page(self, instance):
        self.edit_page.dismiss()

    def open_edit_popup(self, instance):
        self.edit_popup.open()

    def close_edit_popup(self, instance):
        self.edit_popup.dismiss()

    def go_back_button(self, instance):
        el_count.screen_manager.transition = SlideTransition(direction='left')
        el_count.screen_manager.current = "Company"

    def open_popup(self, instance):
        self.add_popup.open()

    def close_popup(self, instance):
        self.add_popup.dismiss()

    def save_info(self, instance):
        try:
            phone_number = int(self.client_phone_number.text)
            Clients.insert(first_name=self.client_first_name.text, last_name=self.client_last_name.text,
                           phone=phone_number, email=self.client_email.text, address=self.client_address.text).execute()
            self.client_first_name.text = self.client_last_name.text = self.client_phone_number.text = ''
            self.client_email.text = self.client_address.text = ''
        except:
            self.close_check_popup(instance)
            self.close_popup(instance)
            self.refresh(instance)
        else:
            self.close_check_popup(instance)
            self.close_popup(instance)
            self.refresh(instance)

    def open_check_popup(self, instance):
        self.check_popup.open()

    def close_check_popup(self, instance):
        self.check_popup.dismiss()

    def refresh(self, instance):
        query = Clients.select().order_by(Clients.id)
        all_tuples = []
        for client in query:
            temp = (client.id, client.first_name, client.last_name, client.phone, client.email, client.address)
            all_tuples.append(temp)
        if len(all_tuples) == 1:
            all_tuples.insert(0, ('', '', '', '', '', ''))
        self.table.row_data = all_tuples


# Project page for displaying and editing data
class ProjectsPage(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.upper = GridLayout()
        self.upper.cols = 3
        self.upper.row_force_default = True
        self.upper.row_default_height = 60
        self.add_widget(self.upper)

        button = Button(text='Go Back...', on_release=self.go_back_button)
        self.upper.add_widget(button)
        self.upper.add_widget(Label())
        button = Button(text='Refresh', on_release=self.refresh)
        self.upper.add_widget(button)

        self.table = MDDataTable(
            pos_hint={'center_x': -100, 'center_y': -100},
            size_hint=(1, 0.8),
            use_pagination=True,
            rows_num=10,
            pagination_menu_height='240dp',
            pagination_menu_pos="auto",
            background_color=[1, 0, 0, .5],

            column_data=[
                ("ID", dp(30)),
                ("Project Name", dp(30)),
                ("Client ID", dp(30)),
                ("Service ID", dp(30)),
                ("Price", dp(30)),
                ("Costs", dp(30)),
                ("Start Date", dp(30)),
                ("End Date", dp(30)),
                ("Manager ID", dp(30))
            ],
            row_data=[]
        )
        self.add_widget(self.table)
        self.refresh(Button())

    def go_back_button(self, instance):
        el_count.screen_manager.transition = SlideTransition(direction='left')
        el_count.screen_manager.current = "Company"

    def open_popup(self, instance):
        self.add_popup.open()

    def close_popup(self, instance):
        self.add_popup.dismiss()

    def refresh(self, instance):
        query = Projects.select().order_by(Projects.id)
        all_tuples = []
        for project in query:
            temp = (project.id, project.project_name, project.client_id, project.service_id, project.price,
                    project.costs, project.start_date, project.end_date, project.manager_id)
            all_tuples.append(temp)
        if len(all_tuples) == 1:
            all_tuples.insert(0, ('', '', '', '', '', '', '', '', ''))
        self.table.row_data = all_tuples


class ElCountApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.screen_manager = ScreenManager()

        self.main_page = MainPage()
        screen = Screen(name='Main')
        screen.add_widget(self.main_page)
        self.screen_manager.add_widget(screen)

        self.company_page = CompanyPage()
        screen = Screen(name='Company')
        screen.add_widget(self.company_page)
        self.screen_manager.add_widget(screen)

        self.employees_page = EmployeesPage()
        screen = Screen(name='EmployeesPage')
        screen.add_widget(self.employees_page)
        self.screen_manager.add_widget(screen)

        self.services_page = ServicesPage()
        screen = Screen(name='Services')
        screen.add_widget(self.services_page)
        self.screen_manager.add_widget(screen)

        self.clients_page = ClientsPage()
        screen = Screen(name='Clients')
        screen.add_widget(self.clients_page)
        self.screen_manager.add_widget(screen)

        self.projects_page = ProjectsPage()
        screen = Screen(name='Projects')
        screen.add_widget(self.projects_page)
        self.screen_manager.add_widget(screen)

        self.accounting_page = AccountingPage()
        screen = Screen(name='Accounting')
        screen.add_widget(self.accounting_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    el_count = ElCountApp()
    el_count.run()
