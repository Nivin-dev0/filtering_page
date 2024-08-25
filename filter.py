import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table as ReportLabTable, TableStyle,SimpleDocTemplate
from reportlab.lib import colors
from reportlab.lib.units import inch
import requests
from streamlit_option_menu import option_menu
from streamlit_extras.stylable_container import stylable_container
from pathlib import Path
from borb.pdf.document.document import Document
from borb.pdf.page.page import Page
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable as Table
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.pdf import PDF
from borb.pdf.canvas.color.color import HexColor
from decimal import Decimal
from streamlit_pdf_viewer import pdf_viewer

# API Adress around Line 77

st.set_page_config(page_title="Data",layout="wide")

# --- PDF Export Function ---
def print_pdf():
    custom = (20 * inch, 10 * inch)
    pdf = SimpleDocTemplate("Data/export.pdf", pagesize=custom, topMargin=0.3*inch, bottomMargin=0.2*inch)
    table_data = []  # Start with the column headers
    table_data.append(columns_selection)
    for i, row in fildata.iterrows():
        table_data.append(list(row))
    table = ReportLabTable(table_data)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ])

    table.setStyle(table_style)
    pdf_table = []
    pdf_table.append(table)
    pdf.build(pdf_table)
    
colm1, colm2, colm3 = st.columns([1, 3, 1])
with colm2:
    selected = option_menu(
        menu_title=None,
        options=["Search", "Personal info"],
        icons=["search", "file-earmark-person"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"background-color": "transparent"},
            "icon": {"color": "ST_COLOR_PALETTE"},
            "nav-link-selected": {"background-color": "ST_COLOR_PALETTE"},
        }
    )

# --- Load Data ---
with st.spinner('Getting Info...'):
    try:
        # --- API Acess Here ---
        indata = requests.get('https://filter-api.glitch.me/api/users').json()
        flattened_data = []
        for item in indata:
            details = item.get("details", {})
            combined_info = {
                #interchanges user_details and personal info inorder to append latest name to the list
                **details.get("personal_info_1", {}),
                **details.get("user_details", {}),
                **details.get("personal_info_2", {}),
                **details.get("personal_info_3", {}),
                **details.get("abuses_faced", {}),
                **details.get("social_status_of_differentially_abled", {}),
                **details.get("economic_status", {}),
                **details.get("education_status", {}),
                **details.get("health_status_1", {}),
                **details.get("health_status_2", {}),
                **details.get("rehabilation_needs", {}),
                **details.get("barriers_felt_at_home", {}),
                **details.get("barriers_felt_at_public_space", {}),
            }
            flattened_data.append(combined_info)
        df = pd.DataFrame(flattened_data)
        #enable this comment to see all data
        #st.write(df)
        df.columns = [
            "Name",
            "Age",
            "Address",
            "Phone No",
            "Ward No",
            "house_no",
            "Gender",
            "E-mail",
            "mobile",
            "Caretaker",
            "caretaker_phone_no",
            "guardian_name",
            "no_of_family_members",
            "parental_status",
            "martial_status",
            "Aadhar No",
            "medical_board_certificate",
            "UID_card",
            "UID_card_no",
            "reason",
            "reason_option",
            "type_of_disablity",
            "percentage_of_disablity",
            "Level of Disability",
            "guardianship",
            "continuous_support_for_ADL_needed",
            "physical_valence",
            "source_of_abuse",
            "mental_abuse",
            "source_of_mental_abuse",
            "Category",
            "classification",
            "Religion",
            "social_protection_yes_or_no",
            "social_protection",
            "participation_yes_or_no",
            "participation",
            "participation_in_family_decision",
            "freedom_for_personnel_decision",
            "ownership_of_assests_yes_or_no",
            "ownership_of_assests",
            "status_of_accommodation",
            "type_of_house",
            "employment",
            "vocational_assessment_conducted",
            "employment_skill",
            "training_needs",
            "financial_need",
            "personal_income",
            "annual_income",
            "educational_level",
            "strain_associated_during_education",
            "category_of_educational_institution",
            "whether_vocational_training_received_yes_or_no",
            "whether_vocational_training_received",
            "are_you_a_member_of_government_institution",
            "government_institution",
            "mark",
            "received_assistance_from_CMDRF_or_KSSM",
            "have_you_taken_compulsory_immunisation",
            "type_of_health_method_you_mainly_adopt",
            "do_you_regularly_depend_on_medicine_yes_or_no",
            "type",
            "recurring_ailments_if_any_mention",
            "in_case_of_children_nutritional_status",
            "any_development_delay_identified",
            "do_you_experience_any_problem_under_intellectual_capacity",
            "do_you_have_any_locomotor_problem",
            "comorbidity",
            "the_assistance_required_to_overcome_the_problem",
            "the_skill_acquired_in_arts_or_sports_if_any_yes_or_no",
            "skill_area",
            "if_talented_why_not_trained",
            "professional_course_completed",
            "completed_vocational_area",
            "non_availability_of_rehabilitation_on_support",
            "barrier_free_physical_facilities_at_home",
            "if_not_BFE_the_deficiency",
            "availability_of_disabled_friendly_toilets",
            "whether_family_permit_to_travel_outside",
            "do_you_participate_decision_making_at_home_yes_or_no",
            "if_not_why",
            "do_you_go_outside_for_personnel_purpose_yes_or_no",
            "if_yes_where_do_you_visit",
            "if_you_do_not_visit_places_why",
            "is_your_workplace_differently_abled_friendly",
            "whether_the_private_institutions_are_differently_abled",
            "can_you_give_the_names_of_places_not_differently_adled_friendly",
            "which_are_the_places_that_to_be_converted_friendly_immediately"
            ]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        df = pd.DataFrame()  # Empty DataFrame on error

# --- Menu Bar ---

if selected == "Search":

    # Additional filtering options
    def _additional_filter():
        col11, col12, col13, col14, col15 = st.columns([1, 6, 1, 6, 1])
        with col12:
            global family_selection,disability_selection,medical_selection,percentage_selection,parental_selection
            family_selection = st.slider('No.of Family Members',
                                        min_value=min(family_members),
                                        max_value=max(family_members),
                                        value=(min(family_members), max(family_members)))
            disability_selection = st.multiselect('Type of Disability',
                                                  type_of_disabilities,
                                                  default=type_of_disabilities)
        with col14:
            medical_selection = st.multiselect('Medical Certificate Status',
                                               medical_certificate,
                                               default=medical_certificate)
            percentage_selection = st.multiselect('Percentage of Disability',
                                                  percentage_disabilities,
                                                  default=percentage_disabilities)
        col21, col22, col23 = st.columns([1, 4, 1])
        with col22:
            parental_selection = st.multiselect('Parental Status',
                                                parental_status,
                                                default=parental_status)
            
    # Abuses faced filtering options
    def _abuses_filter():
        
        col11, col12, col13, col14, col15 = st.columns([1, 6, 1, 6, 1])
        with col12:
            global violence_selection,source_selection,mental_selection,source_mental_selection
            violence_selection = st.multiselect('Physical Violence',
                                                  violence_status,
                                                  default=violence_status)
            source_selection = st.multiselect('Source of Abuse',
                                                  source_abuse,
                                                  default=source_abuse)
        with col14:
            mental_selection = st.multiselect('Mental Abuse',
                                               mental_abuse,
                                               default=mental_abuse)
            source_mental_selection = st.multiselect('Source of Mental abuse',
                                                  source_mental_abuse,
                                                  default=source_mental_abuse)
            
    # Social Status filtering options
    def _social_filter():
        col11, col12, col13, col14, col15 = st.columns([1, 6, 1, 6, 1])
        with col12:
            global categories_selection,classifications_selection,social_selection,participation_y_n_selection,religions_selection,social_protection_selection,participation_y_n_selection,participations_selection,freedom_selection,participations_family_selection
            categories_selection = st.multiselect('Category',
                                                  categories,
                                                  default=categories)
            classifications_selection = st.multiselect('Classification',
                                                  classifications,
                                                  default=classifications)
            social_selection = st.multiselect('Social Protection',
                                                  social_protection_y_n,
                                                  default=social_protection_y_n)
            participation_y_n_selection = st.multiselect('Participation',
                                                  participation_y_n,
                                                  default=participation_y_n)
        with col14:
            religions_selection = st.multiselect('Religion',
                                               religions,
                                               default=religions)
            social_protection_selection = st.multiselect('Social protections',
                                                  social_protections,
                                                  default=social_protections)
            participations_selection = st.multiselect('Participations',
                                                  participations,
                                                  default=participations)
            participations_family_selection = st.multiselect('Participation in family decision',
                                                  participation_family_y_n,
                                                  default=participation_family_y_n)
        col21, col22, col23 = st.columns([1, 4, 1])
        with col22:
            freedom_selection = st.multiselect('Freedom for personal decision',
                                                freedom_personal_decision,
                                                default=freedom_personal_decision)
            
    # Economic Status filtering options
    def _economic_filter():
        col11, col12, col13, col14, col15 = st.columns([1, 6, 1, 6, 1])
        with col12:
            global personal_income_selection,asset_status_selection,status_of_accomodation_selection,type_of_house_selection,employment_status_selection,annual_income_selection,ownership_assets_selection,employement_skills_selection,financial_needs_selection,vocational_assesment_conducted_selection,training_needs_selection
            personal_income_selection = st.slider('Personal Income',
                                        min_value=2000,
                                        max_value=100000,
                                        value=(2000, 100000))
            asset_status_selection = st.multiselect('Ownership of assets',
                                                  asset_status,
                                                  default=asset_status)
            status_of_accomodation_selection = st.multiselect('Status Of Accomodation',
                                                  status_of_accomodation,
                                                  default=status_of_accomodation)
            type_of_house_selection = st.multiselect('Type Of House',
                                                  type_of_house,
                                                  default=type_of_house)
            employment_status_selection = st.multiselect('Employment Status',
                                                  employment_status,
                                                  default=employment_status)
        with col14:
            annual_income_selection = st.slider('Annual Income',
                                        min_value=100000,
                                        max_value=2000000,
                                        value=(10000, 2000000))
            ownership_assets_selection = st.multiselect('Ownership Assets',
                                               ownership_assets,
                                               default=ownership_assets)
            employement_skills_selection = st.multiselect('Employement Skilla',
                                                  employement_skills,
                                                  default=employement_skills)
            financial_needs_selection = st.multiselect('Financial Needs',
                                                  financial_needs,
                                                  default=financial_needs)
            vocational_assesment_conducted_selection = st.multiselect('Vocational Assesment conducted',
                                                  vocational_assesment_conducted,
                                                  default=vocational_assesment_conducted)
        col21, col22, col23 = st.columns([1, 4, 1])
        with col22:
            training_needs_selection = st.multiselect('Training Needs',
                                                training_needs,
                                                default=training_needs)
    # Education Status filtering options
    def _education_filter():
        col11, col12, col13, col14, col15 = st.columns([1, 6, 1, 6, 1])
        with col12:
            global education_level_selection,strain_associated_during_education_selection,category_of_educational_insitution_selection,whether_vocation_training_y_n_selection,vocational_training_recieved_selection
            education_level_selection = st.multiselect('Type of Disability',
                                                  education_level,
                                                  default=education_level)
            strain_associated_during_education_selection = st.multiselect('Type of Disability',
                                                  strain_associated_during_education,
                                                  default=strain_associated_during_education)
        with col14:
            category_of_educational_insitution_selection = st.multiselect('Medical Certificate Status',
                                               category_of_educational_insitution,
                                               default=category_of_educational_insitution)
            whether_vocation_training_y_n_selection = st.multiselect('Percentage of Disability',
                                                  whether_vocation_training_y_n,
                                                  default=whether_vocation_training_y_n)
        col21, col22, col23 = st.columns([1, 4, 1])
        with col22:
            vocational_training_recieved_selection = st.multiselect('Parental Status',
                                                vocational_training_recieved,
                                                default=vocational_training_recieved)
    # Health Status filtering options
    def _health_filter():
        col11, col12, col13, col14, col15 = st.columns([1, 6, 1, 6, 1])
        with col12:
            global are_you_a_member_of_government_institution_selection,government_institution_selection,mark_selection,received_assistance_from_CMDRF_or_KSSM_selection,have_you_taken_compulsory_immunisation_selection,type_of_health_method_you_mainly_adopt_selection,do_you_regularly_depend_on_medicine_yes_or_no_selection,type_selection,recurring_ailments_if_any_mention_selection,in_case_of_children_nutritional_status_selection,any_development_delay_identified_selection,do_you_experience_any_problem_under_intellectual_capacity_selection,do_you_have_any_locomotor_problem_selection,comorbidity_selection
            are_you_a_member_of_government_institution_selection = st.multiselect('Are you a member of government institution?',
                                                  are_you_a_member_of_government_institution,
                                                  default=are_you_a_member_of_government_institution)
            government_institution_selection = st.multiselect('Government Institution',
                                               government_institution,
                                               default=government_institution)
            mark_selection = st.multiselect('Mark',
                                                  mark,
                                                  default=mark)
            received_assistance_from_CMDRF_or_KSSM_selection = st.multiselect('Recieved Assistance from CMDRF or KSSM',
                                               received_assistance_from_CMDRF_or_KSSM,
                                               default=received_assistance_from_CMDRF_or_KSSM)
            have_you_taken_compulsory_immunisation_selection = st.multiselect('Taken compulsary immunization',
                                                  have_you_taken_compulsory_immunisation,
                                                  default=have_you_taken_compulsory_immunisation)
            type_of_health_method_you_mainly_adopt_selection = st.multiselect('Health method mainly adopt',
                                               type_of_health_method_you_mainly_adopt,
                                               default=type_of_health_method_you_mainly_adopt)
            do_you_regularly_depend_on_medicine_yes_or_no_selection = st.multiselect('Regularly Depend on Medicine',
                                                  do_you_regularly_depend_on_medicine_yes_or_no,
                                                  default=do_you_regularly_depend_on_medicine_yes_or_no)
        with col14:
            type_selection = st.multiselect('Type',
                                               type,
                                               default=type)
            recurring_ailments_if_any_mention_selection = st.multiselect('Recurring Ailments',
                                                  recurring_ailments_if_any_mention,
                                                  default=recurring_ailments_if_any_mention)
            in_case_of_children_nutritional_status_selection = st.multiselect('Children nutritional status',
                                               in_case_of_children_nutritional_status,
                                               default=in_case_of_children_nutritional_status)
            any_development_delay_identified_selection = st.multiselect('Development delay identified',
                                                  any_development_delay_identified,
                                                  default=any_development_delay_identified)
            do_you_experience_any_problem_under_intellectual_capacity_selection = st.multiselect('Problem under intellectual capacity',
                                               do_you_experience_any_problem_under_intellectual_capacity,
                                               default=do_you_experience_any_problem_under_intellectual_capacity)
            do_you_have_any_locomotor_problem_selection = st.multiselect('Locomotor Problem',
                                                  do_you_have_any_locomotor_problem,
                                                  default=do_you_have_any_locomotor_problem)
            comorbidity_selection = st.multiselect('Comorbidity',
                                               comorbidity,
                                               default=comorbidity)
            
    # Rehabilation Needs filtering options
    def _rehabilation_filter():
        col11, col12, col13, col14, col15 = st.columns([1, 6, 1, 6, 1])
        with col12:
            global the_assistance_required_to_overcome_the_problem_selection,the_assistance_required_to_overcome_the_problem_selection,the_skill_acquired_in_arts_or_sports_if_any_yes_or_no_selection,skill_area_selection,if_talented_why_not_trained_selection,professional_course_completed_selection,completed_vocational_area_selection,non_availability_of_rehabilitation_on_support_selection
            the_assistance_required_to_overcome_the_problem_selection = st.multiselect('Assistance Required to overcome',
                                                  the_assistance_required_to_overcome_the_problem,
                                                  default=the_assistance_required_to_overcome_the_problem)
            the_skill_acquired_in_arts_or_sports_if_any_yes_or_no_selection = st.multiselect('Skill acquired in Arts/Sports',
                                                  the_skill_acquired_in_arts_or_sports_if_any_yes_or_no,
                                                  default=the_skill_acquired_in_arts_or_sports_if_any_yes_or_no)
            skill_area_selection = st.multiselect('Skill Area',
                                                  skill_area,
                                                  default=skill_area)
        with col14:
            if_talented_why_not_trained_selection = st.multiselect('Why not trained',
                                               if_talented_why_not_trained,
                                               default=if_talented_why_not_trained)
            professional_course_completed_selection = st.multiselect('Professional Courses completed',
                                                  professional_course_completed,
                                                  default=professional_course_completed)
            completed_vocational_area_selection = st.multiselect('Completed Vocational Area',
                                                  completed_vocational_area,
                                                  default=completed_vocational_area)
        col21, col22, col23 = st.columns([1, 4, 1])
        with col22:
            non_availability_of_rehabilitation_on_support_selection = st.multiselect('Non availabilty of rehabitalation support',
                                                non_availability_of_rehabilitation_on_support,
                                                default=non_availability_of_rehabilitation_on_support)
            
    # Barriers felt at home filtering options
    def _barriers_filter():
        
        col11, col12, col13, col14, col15 = st.columns([1, 6, 1, 6, 1])
        with col12:
            global barrier_free_physical_facilities_at_home_selection,if_not_BFE_the_deficiency_selection,availability_of_disabled_friendly_toilets_selection,whether_family_permit_to_travel_outside_selection,do_you_participate_decision_making_at_home_yes_or_no_selection,if_not_why_selection,do_you_go_outside_for_personnel_purpose_yes_or_no_selection,if_yes_where_do_you_visit_selection,if_you_do_not_visit_places_why_selection,is_your_workplace_differently_abled_friendly_selection,whether_the_private_institutions_are_differently_abled_selection,can_you_give_the_names_of_places_not_differently_adled_friendly_selection,which_are_the_places_that_to_be_converted_friendly_immediately_selection
            barrier_free_physical_facilities_at_home_selection = st.multiselect('Barrier free physical facilities at home',
                                                  barrier_free_physical_facilities_at_home,
                                                  default=barrier_free_physical_facilities_at_home)
            if_not_BFE_the_deficiency_selection = st.multiselect('The deficiency',
                                                  if_not_BFE_the_deficiency,
                                                  default=if_not_BFE_the_deficiency)
            availability_of_disabled_friendly_toilets_selection = st.multiselect('Availability of disabled friendly toilets',
                                                  availability_of_disabled_friendly_toilets,
                                                  default=availability_of_disabled_friendly_toilets)
            whether_family_permit_to_travel_outside_selection = st.multiselect('Whether family permits to travel outside',
                                                  whether_family_permit_to_travel_outside,
                                                  default=whether_family_permit_to_travel_outside)
            do_you_participate_decision_making_at_home_yes_or_no_selection = st.multiselect('Participation in decision making at home',
                                                  do_you_participate_decision_making_at_home_yes_or_no,
                                                  default=do_you_participate_decision_making_at_home_yes_or_no)
            if_not_why_selection = st.multiselect('If not why',
                                                  if_not_why,
                                                  default=if_not_why)
        with col14:
            do_you_go_outside_for_personnel_purpose_yes_or_no_selection = st.multiselect('Go outside for personal purposes',
                                               do_you_go_outside_for_personnel_purpose_yes_or_no,
                                               default=do_you_go_outside_for_personnel_purpose_yes_or_no)
            if_yes_where_do_you_visit_selection = st.multiselect('Where do they visit',
                                                  if_yes_where_do_you_visit,
                                                  default=if_yes_where_do_you_visit)
            if_you_do_not_visit_places_why_selection = st.multiselect('Reasons why not visit places',
                                                  if_you_do_not_visit_places_why,
                                                  default=if_you_do_not_visit_places_why)
            is_your_workplace_differently_abled_friendly_selection = st.multiselect('Workplace DA freindly',
                                                  is_your_workplace_differently_abled_friendly,
                                                  default=is_your_workplace_differently_abled_friendly)
            whether_the_private_institutions_are_differently_abled_selection = st.multiselect('Private institutions DA friendly',
                                                  whether_the_private_institutions_are_differently_abled,
                                                  default=whether_the_private_institutions_are_differently_abled)
            can_you_give_the_names_of_places_not_differently_adled_friendly_selection = st.multiselect('Places that are not disabled friendly',
                                                  can_you_give_the_names_of_places_not_differently_adled_friendly,
                                                  default=can_you_give_the_names_of_places_not_differently_adled_friendly)
        col21, col22, col23 = st.columns([1, 4, 1])
        with col22:
            which_are_the_places_that_to_be_converted_friendly_immediately_selection = st.multiselect('Places to be converted DA friendly',
                                                which_are_the_places_that_to_be_converted_friendly_immediately,
                                                default=which_are_the_places_that_to_be_converted_friendly_immediately)
    
    with st.spinner('Displaying...'):
        columns_list = df.columns.tolist()
        columns_default = ['Name', 'Age', 'Address', 'Phone No', 'Ward No', 'Gender', 'Aadhar No', 'Level of Disability', 'Category', 'Religion', 'E-mail', 'Caretaker']

        # Data selections
        marital_status = df['martial_status'].unique().tolist()
        ages = df['Age'].unique().tolist()
        #ageint = [eval(i) for i in ages]
        ward_no = df['Ward No'].unique().astype(int).tolist()
        ward_no.sort()
        genders = df['Gender'].unique().tolist()
        level_disabilities = df['Level of Disability'].unique().tolist()

        # Additional Filtering Data access
        parental_status = df['parental_status'].unique().tolist()
        family_members = df['no_of_family_members'].unique().astype(int).tolist()
        medical_certificate = df['medical_board_certificate'].unique().tolist()
        type_of_disabilities = df['type_of_disablity'].unique().tolist()
        percentage_disabilities = df['percentage_of_disablity'].unique().tolist()
        
        disability_selection = type_of_disabilities
        medical_selection = medical_certificate
        percentage_selection = percentage_disabilities
        parental_selection = parental_status

        # Abuses Filtering Data Acess
        violence_status = df['physical_valence'].unique().tolist()
        source_abuse = df['source_of_abuse'].unique().tolist()
        mental_abuse = df['mental_abuse'].unique().tolist()
        source_mental_abuse = df['source_of_mental_abuse'].unique().tolist()

        violence_selection = violence_status
        source_selection = source_abuse
        mental_selection = mental_abuse
        source_mental_selection = source_mental_abuse

        # Social Status filtering Data Access
        categories = df['Category'].unique().tolist()
        #family_members = df['no_of_family_members'].unique().astype(int).tolist()
        classifications = df['classification'].unique().tolist()
        religions = df['Religion'].unique().tolist()
        social_protection_y_n = df['social_protection_yes_or_no'].unique().tolist()
        social_protections = df['social_protection'].unique().tolist()
        participation_y_n = df['participation_yes_or_no'].unique().tolist()
        participations = df['participation'].unique().tolist()
        participation_family_y_n = df['participation_in_family_decision'].unique().tolist()
        freedom_personal_decision = df['freedom_for_personnel_decision'].unique().tolist()

        categories_selection=categories
        classifications_selection=classifications
        social_selection=social_protection_y_n
        participation_y_n_selection=participation_y_n
        religions_selection=religions
        social_protection_selection=social_protections
        participations_selection=participations
        participations_family_selection=participation_family_y_n
        freedom_selection=freedom_personal_decision

        # Economic Status filtering data acess
        asset_status = df['ownership_of_assests_yes_or_no'].unique().tolist()
        # = df['personal_income'].unique().astype(int).tolist()
        ownership_assets = df['ownership_of_assests'].unique().tolist()
        status_of_accomodation = df['status_of_accommodation'].unique().tolist()
        type_of_house = df['type_of_house'].unique().tolist()
        employment_status = df['employment'].unique().tolist()
        #annual_income = df['annual_income'].unique().astype(int).tolist()
        vocational_assesment_conducted = df['vocational_assessment_conducted'].unique().tolist()
        employement_skills = df['employment_skill'].unique().tolist()
        training_needs = df['training_needs'].unique().tolist()
        financial_needs = df['financial_need'].unique().tolist()

        asset_status_selection = asset_status
        status_of_accomodation_selection = status_of_accomodation
        type_of_house_selection = type_of_house
        employment_status_selection = employment_status
        #annual_income_selection
        ownership_assets_selection = ownership_assets
        employement_skills_selection = employement_skills
        financial_needs_selection = financial_needs
        vocational_assesment_conducted_selection = vocational_assesment_conducted
        training_needs_selection = training_needs

        # Education status filtering Data Acess
        education_level = df['educational_level'].unique().tolist()
        strain_associated_during_education = df['strain_associated_during_education'].unique().tolist()
        category_of_educational_insitution = df['category_of_educational_institution'].unique().tolist()
        whether_vocation_training_y_n = df['whether_vocational_training_received_yes_or_no'].unique().tolist()
        vocational_training_recieved = df['whether_vocational_training_received'].unique().tolist()
        
        education_level_selection = education_level
        strain_associated_during_education_selection = strain_associated_during_education
        category_of_educational_insitution_selection = category_of_educational_insitution
        whether_vocation_training_y_n_selection = whether_vocation_training_y_n
        vocational_training_recieved_selection = vocational_training_recieved

        # Health status filtering Data Acess
        are_you_a_member_of_government_institution = df['are_you_a_member_of_government_institution'].unique().tolist()
        government_institution = df['government_institution'].unique().tolist()
        mark = df['mark'].unique().tolist()
        received_assistance_from_CMDRF_or_KSSM = df['received_assistance_from_CMDRF_or_KSSM'].unique().tolist()
        have_you_taken_compulsory_immunisation = df['have_you_taken_compulsory_immunisation'].unique().tolist()
        type_of_health_method_you_mainly_adopt = df['type_of_health_method_you_mainly_adopt'].unique().tolist()
        do_you_regularly_depend_on_medicine_yes_or_no = df['do_you_regularly_depend_on_medicine_yes_or_no'].unique().tolist()
        type = df['type'].unique().tolist()
        recurring_ailments_if_any_mention = df['recurring_ailments_if_any_mention'].unique().tolist()
        in_case_of_children_nutritional_status = df['in_case_of_children_nutritional_status'].unique().tolist()
        any_development_delay_identified = df['any_development_delay_identified'].unique().tolist()
        do_you_experience_any_problem_under_intellectual_capacity = df['do_you_experience_any_problem_under_intellectual_capacity'].unique().tolist()
        do_you_have_any_locomotor_problem = df['do_you_have_any_locomotor_problem'].unique().tolist()
        comorbidity = df['comorbidity'].unique().tolist()

        are_you_a_member_of_government_institution_selection = are_you_a_member_of_government_institution
        government_institution_selection = government_institution
        mark_selection = mark
        received_assistance_from_CMDRF_or_KSSM_selection = received_assistance_from_CMDRF_or_KSSM
        have_you_taken_compulsory_immunisation_selection = have_you_taken_compulsory_immunisation
        type_of_health_method_you_mainly_adopt_selection = type_of_health_method_you_mainly_adopt
        do_you_regularly_depend_on_medicine_yes_or_no_selection = do_you_regularly_depend_on_medicine_yes_or_no
        type_selection = type
        recurring_ailments_if_any_mention_selection = recurring_ailments_if_any_mention
        in_case_of_children_nutritional_status_selection = in_case_of_children_nutritional_status
        any_development_delay_identified_selection = any_development_delay_identified
        do_you_experience_any_problem_under_intellectual_capacity_selection = do_you_experience_any_problem_under_intellectual_capacity
        do_you_have_any_locomotor_problem_selection = do_you_have_any_locomotor_problem
        comorbidity_selection = comorbidity

        # Rehabilation needs Data Acess
        the_assistance_required_to_overcome_the_problem = df['the_assistance_required_to_overcome_the_problem'].unique().tolist()
        the_skill_acquired_in_arts_or_sports_if_any_yes_or_no = df['the_skill_acquired_in_arts_or_sports_if_any_yes_or_no'].unique().tolist()
        skill_area = df['skill_area'].unique().tolist()
        if_talented_why_not_trained = df['if_talented_why_not_trained'].unique().tolist()
        professional_course_completed = df['professional_course_completed'].unique().tolist()
        completed_vocational_area = df['completed_vocational_area'].unique().tolist()
        non_availability_of_rehabilitation_on_support = df['non_availability_of_rehabilitation_on_support'].unique().tolist()

        the_assistance_required_to_overcome_the_problem_selection =the_assistance_required_to_overcome_the_problem
        the_skill_acquired_in_arts_or_sports_if_any_yes_or_no_selection =the_skill_acquired_in_arts_or_sports_if_any_yes_or_no
        skill_area_selection =skill_area
        if_talented_why_not_trained_selection =if_talented_why_not_trained
        professional_course_completed_selection =professional_course_completed
        completed_vocational_area_selection =completed_vocational_area
        non_availability_of_rehabilitation_on_support_selection =non_availability_of_rehabilitation_on_support

        #Barriers felt at home Data Acess
        barrier_free_physical_facilities_at_home = df['barrier_free_physical_facilities_at_home'].unique().tolist()
        if_not_BFE_the_deficiency = df['if_not_BFE_the_deficiency'].unique().tolist()
        availability_of_disabled_friendly_toilets = df['availability_of_disabled_friendly_toilets'].unique().tolist()
        whether_family_permit_to_travel_outside = df['whether_family_permit_to_travel_outside'].unique().tolist()
        do_you_participate_decision_making_at_home_yes_or_no = df['do_you_participate_decision_making_at_home_yes_or_no'].unique().tolist()
        which_are_the_places_that_to_be_converted_friendly_immediately = df['which_are_the_places_that_to_be_converted_friendly_immediately'].unique().tolist()
        if_not_why = df['if_not_why'].unique().tolist()
        do_you_go_outside_for_personnel_purpose_yes_or_no = df['do_you_go_outside_for_personnel_purpose_yes_or_no'].unique().tolist()
        if_yes_where_do_you_visit = df['if_yes_where_do_you_visit'].unique().tolist()
        if_you_do_not_visit_places_why = df['if_you_do_not_visit_places_why'].unique().tolist()
        is_your_workplace_differently_abled_friendly = df['is_your_workplace_differently_abled_friendly'].unique().tolist()
        whether_the_private_institutions_are_differently_abled = df['whether_the_private_institutions_are_differently_abled'].unique().tolist()
        can_you_give_the_names_of_places_not_differently_adled_friendly = df['can_you_give_the_names_of_places_not_differently_adled_friendly'].unique().tolist()

        barrier_free_physical_facilities_at_home_selection =barrier_free_physical_facilities_at_home
        if_not_BFE_the_deficiency_selection =if_not_BFE_the_deficiency
        availability_of_disabled_friendly_toilets_selection =availability_of_disabled_friendly_toilets
        whether_family_permit_to_travel_outside_selection =whether_family_permit_to_travel_outside
        do_you_participate_decision_making_at_home_yes_or_no_selection =do_you_participate_decision_making_at_home_yes_or_no
        if_not_why_selection =if_not_why
        do_you_go_outside_for_personnel_purpose_yes_or_no_selection =do_you_go_outside_for_personnel_purpose_yes_or_no
        if_yes_where_do_you_visit_selection =if_yes_where_do_you_visit
        if_you_do_not_visit_places_why_selection =if_you_do_not_visit_places_why
        is_your_workplace_differently_abled_friendly_selection =is_your_workplace_differently_abled_friendly
        whether_the_private_institutions_are_differently_abled_selection =whether_the_private_institutions_are_differently_abled
        can_you_give_the_names_of_places_not_differently_adled_friendly_selection =can_you_give_the_names_of_places_not_differently_adled_friendly
        which_are_the_places_that_to_be_converted_friendly_immediately_selection =which_are_the_places_that_to_be_converted_friendly_immediately



        with st.form(key='filtered_view', border=False):
            with st.expander("Filter By"):
                col11, col12, col13, col14, col15 = st.columns([1, 6, 1, 6, 1])
                with col12:
                    age_selection = st.slider('Age:',
                                              min_value=18,
                                              max_value=60,
                                              value=(18,60))
                    marital_selection = st.multiselect('Marital Status',
                                                       marital_status,
                                                       default=marital_status)
                with col14:
                    gender_selection = st.multiselect('Gender',
                                                      genders,
                                                      default=genders)
                    level_selection = st.multiselect('Level of Disability',
                                                     level_disabilities,
                                                     default=level_disabilities)
                col21, col22, col23 = st.columns([1, 4, 1])
                with col22:
                    ward_selection = st.multiselect('Ward',
                                                    ward_no,
                                                    default=ward_no)
                on = st.checkbox("Show Additional options")
                if on:
                    _additional_filter()
                af = st.checkbox("Abuses Faced")
                if af:
                    _abuses_filter()
                ss = st.checkbox("Social Status")
                if ss:
                    _social_filter()
                es = st.checkbox("Economic Status")
                if es:
                    _economic_filter()
                ed = st.checkbox("Education Status")
                if ed:
                    _education_filter()
                hs = st.checkbox("Health Status")
                if hs:
                    _health_filter()
                rn = st.checkbox("Rehabilation Needs")
                if rn:
                    _rehabilation_filter()
                bf  = st.checkbox("Barriers felt at home")
                if bf:
                    _barriers_filter()
                st.write()
                st.markdown("*Please click on apply changes after clicking checkboxes*")
                


            col1, col2 = st.columns([3, 1])
            with col1:
                with st.expander("Display"):
                    columns_selection = st.multiselect('Select Columns to Display',
                                                        columns_list,
                                                        default=columns_default)
            with col2:
                submit_button = st.form_submit_button(label='Apply Changes', use_container_width=True)

    # Filtered DataFrame

    #(df['no_of_family_members'].isin()) &\
    #(.isin()) &\

    mask = (df['martial_status'].isin(marital_selection)) & \
           (df['Gender'].isin(gender_selection)) & \
           (df['Level of Disability'].isin(level_selection)) &\
           (df['Ward No'].isin(ward_selection)) &\
           (df['parental_status'].isin(parental_selection)) &\
           (df['medical_board_certificate'].isin(medical_selection)) &\
           (df['type_of_disablity'].isin(disability_selection)) &\
           (df['percentage_of_disablity'].isin(percentage_selection)) &\
           (df['physical_valence'].isin(violence_selection)) &\
           (df['source_of_abuse'].isin(source_selection)) &\
           (df['mental_abuse'].isin(mental_selection)) &\
           (df['source_of_mental_abuse'].isin(source_mental_selection)) &\
           (df['Category'].isin(categories_selection)) &\
           (df['classification'].isin(classifications_selection)) &\
           (df['Religion'].isin(religions_selection)) &\
           (df['social_protection_yes_or_no'].isin(social_selection)) &\
           (df['social_protection'].isin(social_protection_selection)) &\
           (df['participation_yes_or_no'].isin(participation_y_n)) &\
           (df['participation'].isin(participations_selection)) &\
           (df['participation_in_family_decision'].isin(participations_family_selection)) &\
           (df['freedom_for_personnel_decision'].isin(freedom_personal_decision)) &\
           (df['ownership_of_assests_yes_or_no'].isin(asset_status_selection)) &\
           (df['ownership_of_assests'].isin(ownership_assets_selection)) &\
           (df['status_of_accommodation'].isin(status_of_accomodation_selection)) &\
           (df['type_of_house'].isin(type_of_house_selection)) &\
           (df['employment'].isin(employment_status_selection)) &\
           (df['vocational_assessment_conducted'].isin(vocational_assesment_conducted_selection)) &\
           (df['employment_skill'].isin(employement_skills_selection)) &\
           (df['financial_need'].isin(financial_needs_selection)) &\
           (df['training_needs'].isin(training_needs_selection)) &\
           (df['educational_level'].isin(education_level_selection)) &\
           (df['strain_associated_during_education'].isin(strain_associated_during_education_selection)) &\
           (df['category_of_educational_institution'].isin(category_of_educational_insitution_selection)) &\
           (df['whether_vocational_training_received_yes_or_no'].isin(whether_vocation_training_y_n_selection)) &\
           (df['whether_vocational_training_received'].isin(vocational_training_recieved_selection)) &\
           (df['are_you_a_member_of_government_institution'].isin(are_you_a_member_of_government_institution_selection)) &\
           (df['government_institution'].isin(government_institution_selection)) &\
           (df['mark'].isin(mark_selection)) &\
           (df['received_assistance_from_CMDRF_or_KSSM'].isin(received_assistance_from_CMDRF_or_KSSM_selection)) &\
           (df['have_you_taken_compulsory_immunisation'].isin(have_you_taken_compulsory_immunisation_selection)) &\
           (df['type_of_health_method_you_mainly_adopt'].isin(type_of_health_method_you_mainly_adopt_selection)) &\
           (df['do_you_regularly_depend_on_medicine_yes_or_no'].isin(do_you_regularly_depend_on_medicine_yes_or_no_selection)) &\
           (df['type'].isin(type_selection)) &\
           (df['recurring_ailments_if_any_mention'].isin(recurring_ailments_if_any_mention_selection)) &\
           (df['in_case_of_children_nutritional_status'].isin(in_case_of_children_nutritional_status_selection)) &\
           (df['any_development_delay_identified'].isin(any_development_delay_identified_selection)) &\
           (df['do_you_experience_any_problem_under_intellectual_capacity'].isin(do_you_experience_any_problem_under_intellectual_capacity_selection)) &\
           (df['do_you_have_any_locomotor_problem'].isin(do_you_have_any_locomotor_problem_selection)) &\
           (df['comorbidity'].isin(comorbidity_selection)) &\
           (df['the_assistance_required_to_overcome_the_problem'].isin(the_assistance_required_to_overcome_the_problem_selection)) &\
           (df['the_skill_acquired_in_arts_or_sports_if_any_yes_or_no'].isin(the_skill_acquired_in_arts_or_sports_if_any_yes_or_no_selection)) &\
           (df['skill_area'].isin(skill_area_selection)) &\
           (df['if_talented_why_not_trained'].isin(if_talented_why_not_trained_selection)) &\
           (df['professional_course_completed'].isin(professional_course_completed_selection)) &\
           (df['completed_vocational_area'].isin(completed_vocational_area_selection)) &\
           (df['non_availability_of_rehabilitation_on_support'].isin(non_availability_of_rehabilitation_on_support_selection)) &\
           (df['barrier_free_physical_facilities_at_home'].isin(barrier_free_physical_facilities_at_home_selection)) &\
           (df['if_not_BFE_the_deficiency'].isin(if_not_BFE_the_deficiency_selection)) &\
           (df['availability_of_disabled_friendly_toilets'].isin(availability_of_disabled_friendly_toilets_selection)) &\
           (df['whether_family_permit_to_travel_outside'].isin(whether_family_permit_to_travel_outside_selection)) &\
           (df['do_you_participate_decision_making_at_home_yes_or_no'].isin(do_you_participate_decision_making_at_home_yes_or_no_selection)) &\
           (df['which_are_the_places_that_to_be_converted_friendly_immediately'].isin(which_are_the_places_that_to_be_converted_friendly_immediately_selection))&\
           (df['if_not_why'].isin(if_not_why_selection)) &\
           (df['do_you_go_outside_for_personnel_purpose_yes_or_no'].isin(do_you_go_outside_for_personnel_purpose_yes_or_no_selection)) &\
           (df['if_yes_where_do_you_visit'].isin(if_yes_where_do_you_visit_selection)) &\
           (df['if_you_do_not_visit_places_why'].isin(if_you_do_not_visit_places_why_selection)) &\
           (df['is_your_workplace_differently_abled_friendly'].isin(is_your_workplace_differently_abled_friendly_selection)) &\
           (df['can_you_give_the_names_of_places_not_differently_adled_friendly'].isin(can_you_give_the_names_of_places_not_differently_adled_friendly_selection)) &\
           (df['whether_the_private_institutions_are_differently_abled'].isin(whether_the_private_institutions_are_differently_abled_selection))
    
    number_of_result = df[mask].shape[0]
    st.markdown(f'*Available Results: {number_of_result}*')
    fildata = df[mask][columns_selection].reset_index(drop=True)
    st.dataframe(fildata)

    if st.button("Export Data", type='primary'):
        with st.spinner('Generating...'):
            print_pdf()
            with open("Data/export.pdf", "rb") as pdf_file:
                PDFbyte = pdf_file.read()
                st.download_button(label="Download PDF",
                                   data=PDFbyte,
                                   file_name="Exported.pdf",
                                   mime='application/octet-stream')

if selected == "Personal info":
    # --- Definition of PDF Layout ---
    def _build_first_page():    
        table_001 = Table(number_of_rows=23, number_of_columns=2) 
        table_001.add(Paragraph("Age", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,1]))) 
        table_001.add(Paragraph("Address", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,2])))  
        table_001.add(Paragraph("Phone No", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,3])))  
        table_001.add(Paragraph("Ward No", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,4])))  
        table_001.add(Paragraph("House No", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,5])))  
        table_001.add(Paragraph("Gender", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,6])))  
        table_001.add(Paragraph("CareTaker", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,9])+" Phone No:"+str(df[prsnl].iloc[0,10])))  
        table_001.add(Paragraph("Guardian's Name", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT))
        table_001.add(Paragraph(str(df[prsnl].iloc[0,11])))  
        table_001.add(Paragraph("No.of Family Members", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT))
        table_001.add(Paragraph(str(df[prsnl].iloc[0,12])))
         
        table_001.add(Paragraph("Parental Status", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,13])))  

        table_001.add(Paragraph("Marital Status", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,14])))  

        table_001.add(Paragraph("Aadhar No", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,15]))) 

        table_001.add(Paragraph("Medical Board Certificate", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,16])))  

        table_001.add(Paragraph("")) 
        table_001.add(Paragraph(""))  

        table_001.add(Paragraph("UID Card", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,17])))  

        table_001.add(Paragraph("UID Card Number", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,18])))  

        table_001.add(Paragraph("Type of Disablility", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,21])))  

        table_001.add(Paragraph("Percentage of Disability", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,22])))  

        table_001.add(Paragraph("Level of Disability", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,23])))  
            
        table_001.add(Paragraph("Guardianship", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT))
        table_001.add(Paragraph(str(df[prsnl].iloc[0,24])))  
            
        table_001.add(Paragraph("Continous Support for ADL needed?", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT))
        table_001.add(Paragraph(str(df[prsnl].iloc[0,25])))
        
        table_001.add(Paragraph("Physical Violence", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,26])))  

        table_001.add(Paragraph("Source of Abuse", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,27])))  

        table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))    		
        table_001.no_borders()
        return table_001
    
    def _build_second_page():    
        table_001 = Table(number_of_rows=29, number_of_columns=2) 
        table_001.add(Paragraph("Category", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,28]))) 
        table_001.add(Paragraph("Classification", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,29])))  
        table_001.add(Paragraph("Religion", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,30])))  
        table_001.add(Paragraph("Social Protection Available", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,31])))  
        table_001.add(Paragraph("Social Protection needed", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,32])))  
        table_001.add(Paragraph("Participation ", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,33])))  
        table_001.add(Paragraph("Participations", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,34])+" Phone No:"+str(df[prsnl].iloc[0,10])))  
        table_001.add(Paragraph("Participation in family decisions", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT))
        table_001.add(Paragraph(str(df[prsnl].iloc[0,35])))  
        table_001.add(Paragraph("Freedom for personal decissions", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT))
        table_001.add(Paragraph(str(df[prsnl].iloc[0,36])))
         
        table_001.add(Paragraph("Ownership of assets ?", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,37])))  

        table_001.add(Paragraph("Assets Available", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,38])))  

        table_001.add(Paragraph("Status of accomadation", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,39]))) 

        table_001.add(Paragraph("Type of House", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,40])))  

        table_001.add(Paragraph("")) 
        table_001.add(Paragraph(""))  

        table_001.add(Paragraph("Employment", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,41])))  

        table_001.add(Paragraph("Vocational Assesment conducted?", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,42])))  

        table_001.add(Paragraph("Employment Skill", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,43])))  

        table_001.add(Paragraph("Training needs", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,44])))  

        table_001.add(Paragraph("Financial needs", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,45])))  
            
        table_001.add(Paragraph("Personal Income", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT))
        table_001.add(Paragraph(str(df[prsnl].iloc[0,46])))  
            
        table_001.add(Paragraph("Annual Income", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT))
        table_001.add(Paragraph(str(df[prsnl].iloc[0,47])))
        
        table_001.add(Paragraph("Education Level", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,48])))  

        table_001.add(Paragraph("Strain associated during education", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,49]))) 
        table_001.add(Paragraph("Category of Educational Institution", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,50]))) 
        table_001.add(Paragraph("Vocational training recieved ?", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,51]))) 
        table_001.add(Paragraph("Whether vocational training recieved", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,52]))) 
        table_001.add(Paragraph("Member of Government intitution", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,53])))  
        table_001.add(Paragraph("Government Insitution Name", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,54]))) 
        table_001.add(Paragraph("Mark", font="Helvetica-Bold", horizontal_alignment=Alignment.LEFT)) 
        table_001.add(Paragraph(str(df[prsnl].iloc[0,55]))) 

        table_001.set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))    		
        table_001.no_borders()
        return table_001
    
    col1, col2, col3 = st.columns([4, 1, 6])

    with col1:
        srch_int=0
        srch_code=st.text_input("Aadhar No", value="", max_chars=12)
        if srch_code:
            srch_int=srch_code

        prsnl=(df['Aadhar No']==srch_int)
        if df[prsnl].shape[0]:
            st.markdown(f'Found User')
            st.markdown(f'**{df[prsnl].iloc[0,0]}**')
            with st.spinner('Getting Info...'):
                pdf = Document()
                # Creating Document
                page1=Page()
                page2=Page()
                pdf.add_page(page1)
                page_layout = SingleColumnLayout(page1)
                page_layout.vertical_margin = page1.get_page_info().get_height() * Decimal(0.02)
                page_layout.add(    
                Image(        
                image=Path(r"assets\pbanner.png"),
                
                width=Decimal(466),        
                height=Decimal(68),    
                ))
                # Title
                page_layout.add(
                    Paragraph(
                        str(df[prsnl].iloc[0,0]), font_color=HexColor("#283592"), font_size=Decimal(25)
                    )
                )
                # Invoice information table  
                page_layout.add(_build_first_page())  
            
                # Empty paragraph for spacing  
                page_layout.add(Paragraph(" "))
                # Page 2
                pdf.add_page(page2)
                page_layout = SingleColumnLayout(page2)
                page_layout.vertical_margin = page2.get_page_info().get_height() * Decimal(0.02)
                page_layout.add(_build_second_page())


            with open("Data\cacheout.pdf", "wb") as pdf_file_handle:
                PDF.dumps(pdf_file_handle, pdf)
            with col3:
                with open("Data\cacheout.pdf", "rb") as pdf_file:
                    PDFbyte = pdf_file.read()
                    pdf_viewer(input=PDFbyte,width=700)
                    with col1:
                        st.download_button(label="Download Report",
                                        data=PDFbyte,
                                        file_name=str(df[prsnl].iloc[0,0])+".pdf",
                                        mime='application/octet-stream')
            
        

        elif srch_int==0:
            st.markdown(f'*Enter UID Number*')
        else:
            st.markdown(f'*The person not available or there will be a mistake in data entry*')
