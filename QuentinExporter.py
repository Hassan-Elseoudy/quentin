class QuentinExporter:
    # Required.
    company_url: str = ''
    company_name: str = ''
    activity: str = ''
    company_linked_in: str = ''
    company_founding_year: str = ''
    company_employees: str = ''
    person_full_name: str = ''
    person_job_title: str = ''
    person_url: str = ''
    # Additional info.
    company_title: str = ''
    company_description: str = ''
    company_content: str = ''
    company_main_terms: str = ''
    company_detailed_terms: str = ''
    stats: str = {}

    def __init__(self, company_url: str, company_name: str, activity: str, company_linked_in: str,
                 company_founding_year: str, company_employees: str, person_full_name: str, person_job_title: str,
                 person_url: str, company_title: str, company_description: str, company_content: str, company_main_terms: str,
                 company_detailed_terms: str, stats: {}):
        self.company_url = company_url
        self.company_name = company_name
        self.activity = activity
        self.company_linked_in = company_linked_in
        self.company_founding_year = company_founding_year
        self.company_employees = company_employees
        self.person_full_name = person_full_name
        self.person_job_title = person_job_title
        self.person_url = person_url
        self.company_title = company_title
        self.company_description = company_description
        self.company_content = company_content
        self.company_main_terms = company_main_terms
        self.company_detailed_terms = company_detailed_terms
        self.stats = stats
