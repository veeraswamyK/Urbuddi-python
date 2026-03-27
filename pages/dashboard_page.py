
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):


    DASHBOARD_HEADING = (By.XPATH, "//div[@class='page-header-container']//p[text()='Dashboard']")
    ADD_HOLIDAYS_BTN = (By.XPATH, "//button[contains(text(),'Add Holidays')]")
    ADD_EVENTS_BTN = (By.XPATH, "//button[contains(text(),'Add Events')]")


    NAV_DASHBOARD = (By.XPATH, "//div[@class='left-navigation-container']//p[text()='Dashboard']")
    NAV_EMPLOYEES = (By.XPATH, "//div[@class='left-navigation-container']//p[text()='Employees']")
    NAV_LEAVE_MANAGEMENT = (By.XPATH, "//div[@class='left-navigation-container']//p[text()='Leave Management']")
    NAV_SALARY_MANAGEMENT = (By.XPATH, "//div[@class='left-navigation-container']//p[text()='Salary Management']")
    NAV_PAYSLIP = (By.XPATH, "//div[@class='left-navigation-container']//p[text()='Payslip']")
    NAV_RESOURCE_TRACKING = (By.XPATH, "//p[contains(text(),'Resource Tracking')]")
    NAV_REIMBURSEMENT = (By.XPATH, "//p[contains(text(),'Reimbursement')]")
    NAV_EXPENDITURE = (By.XPATH, "//p[contains(text(),'Expenditure')]")
    NAV_POLICY = (By.XPATH, "//p[contains(text(),'Policies')]")
    NAV_EmailTemplates = (By.XPATH, "//p[contains(text(),'Email Templates')]")
    NAV_Billing = (By.XPATH, "//p[contains(text(),'Billing')]")
    Billing_projects=(By.XPATH, "//p[text()='Projects']")
    Billing_invoices=(By.XPATH, "//p[text()='Invoices']")
    Billing_clients=(By.XPATH, "//p[text()='Projects']")

    BIRTHDAYS_SECTION = (By.XPATH, "//h5[contains(text(),\"Birthday\")]/..")
    BIRTHDAYS_SECTIONS = (By.XPATH, "//h5[contains(text(),\"Birthday\")]/..")
    SECTIONS = (By.XPATH, "//h5[contains(text(),\"Birthday\")]/..")