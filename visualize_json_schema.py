import streamlit as st
import json

static_json="""{
    "extraction_functions_schema": [
        {
            "name": "extract_visa_features",
            "description": "Extracts the specified features from the AAO Decision. Do not make up information. Returns N/A if information is not available. Extract all the information you can find. Do not leave any fields blank.",
            "parameters": {
                "type": "object",
                "properties": {
                    "type_of_visa_petition": {
                        "type": "object",
                        "properties": {
                            "visa_type": {
                                "type": "string",
                                "description": "Full label of the visa type (including the subclass)",
                                "display_name": "Type of Visa"
                            },
                            "Form_Type": {
                                "type": "string",
                                "description": "Form Type",
                                "display_name": "Form Type"
                            }
                        },
                        "display_name": "Type of Visa Petition"
                    },
                    "USCIS_decision": {
                        "type": "object",
                        "properties": {
                            "decision_type": {
                                "type": "string",
                                "enum": [
                                    "Denied (Merits)",
                                    "Dismissed (Procedural)",
                                    "Revoked (Post-Approval)",
                                    "Certified to AAO"
                                ],
                                "display_name": "Initial Decision Type"
                            },
                            "specific_reason": {
                                "type": "string",
                                "description": "Detailed reason(s) for the initial decision (e.g., failure to meet national interest waiver criteria, untimely appeal, missing required documents).",
                                "display_name": "Specific Initial Reason"
                            },
                            "categorical_reason": {
                                "type": "string",
                                "enum": [
                                    "Failure to Meet Eligibility Criteria",
                                    "Insufficient Evidence",
                                    "Discretionary Denial",
                                    "Fraud or Misrepresentation",
                                    "Inadmissibility Issues",
                                    "Public Charge Concerns",
                                    "Failure to Respond",
                                    "Late Filing",
                                    "Jurisdictional Issue",
                                    "Improperly Filed Petition",
                                    "Fraud Post-Approval",
                                    "Change in Employment Terms",
                                    "Consular Return (221g)",
                                    "Other/NA"
                                ],
                                "description": "Generalized category for the initial decision reason.",
                                "display_name": "Categorical Initial Reason"
                            }
                        },
                        "display_name": "USCIS Decision"
                    },
                    "AAO_decision": {
                        "type": "object",
                        "properties": {
                            "outcome": {
                                "type": "string",
                                "enum": [
                                    "Denied",
                                    "Overturned",
                                    "Dismissed",
                                    "Remanded"
                                ],
                                "description": "Final outcome of the case."
                            },
                            "decision_date": {
                                "type": "string",
                                "format": "date",
                                "description": "Date of the decision."
                            },
                            "specific_reason": {
                                "type": "string",
                                "description": "Detailed reason(s) for the AAO decision.",
                                "display_name": "Specific AAO Reason"
                            },
                            "categorical_reason": {
                                "type": "string",
                                "enum": [
                                    "Lack of Evidence",
                                    "Failure to Meet Eligibility Criteria",
                                    "Discretionary Denial",
                                    "Fraud or Misrepresentation",
                                    "National Security or Criminal Grounds",
                                    "Public Charge Concerns",
                                    "Late Filing",
                                    "Jurisdictional Issue",
                                    "Failure to Respond to RFE/NOID",
                                    "Petition Abandoned / withdrawn",
                                    "Improperly Filed Petition",
                                    "Repetitive Arguments",
                                    "Failure to Meet Motion Requirements",
                                    "Procedural Error by USCIS",
                                    "Insufficient Justification for Negative Finding",
                                    "New Evidence Required",
                                    "Meets All Eligibility Requirements",
                                    "Overturned on Appeal",
                                    "RFE/NOID Response Accepted",
                                    "Other/NA"
                                ],
                                "description": "Generalized category for the AAO decision reason.",
                                "display_name": "Categorical Decision Reason"
                            }
                        }
                    },
                    "petitioner_type": {
                        "type": "string",
                        "description": "Petitioner Type: Company, Individual, University, etc.",
                        "display_name": "Petitioner Type"
                    },
                    "job_position": {
                        "type": "object",
                        "properties": {
                            "job_title": {
                                "type": "string",
                                "description": "Job Title (e.g., Software Engineer, Research Scientist)",
                                "display_name": "Job Title"
                            },
                            "industry": {
                                "type": "string",
                                "description": "Industry (e.g., Technology, Healthcare, Academia)",
                                "display_name": "Industry sector"
                            },
                            "SOC_code": {
                                "type": "string",   
                                "description": "Standard Occupational Classification (SOC) code (e.g., 15-1132)",
                                "display_name": "SOC Code"
                            }
                        },
                        "display_name": "Job Position"
                    },
                    "positive_factors": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Positive Factors (e.g., Family ties, economic contribution, research grants, etc.)",
                        "display_name": "Positive Factors"
                    },
                    "negative_factors": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Negative Factors (e.g., Immigration violations, criminal history, etc.)",
                        "display_name": "Negative Factors"
                    },
                    "nationalities": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Nationalities of the beneficiary (Countries of citizenship)",
                        "display_name": "Nationalities"
                    },
                    "legal_citations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {
                                    "type": "string",
                                    "description": "Legal text (e.g., '8 CFR § 214.2(h)(11)(iii)')."
                                },
                                "context": {
                                    "type": "string",
                                    "description": "Brief desription of how it was applied (e.g., 'Denied H-1B due to specialty occupation criteria')."
                                }
                            }
                        }
                    },
                    "precedent_citations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "case_name": {
                                    "type": "string",
                                    "description": "The precedent AAO Decision (e.g., Matter of Dhanasar)."
                                },
                                "context": {
                                    "type": "string",
                                    "description": "Provide detail why this precedent was cited (e.g., burden of proof, de novo review, national interest standard)."
                                }
                            }
                        },
                        "description": "ALL Precedent AAO Decisions citated with contextual explanations.",
                        "display_name": "Precedent Citations"
                    },
                    "visa_requirements": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Visa Requirements (Eligibility criteria cited in the decision)",
                        "display_name": "Visa Requirements"
                    },
                    "specific_criteria_argued": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "criteria": {
                                    "type": "string",
                                    "enum": [
                                        "Educational documents",
                                        "One-Time Achievement",
                                        "Awards and prizes",
                                        "Membership in Professional Associations",
                                        "Media or press about the applicant",
                                        "Original contributions",
                                        "Scholarly Publications",
                                        "Employment in critical capacity",
                                        "Command a high salary",
                                        "Comparable Evidence",
                                        "Artistic contributions",
                                        "Performing arts contributions",
                                        "Employer Documents",
                                        "Information about area of expertise",
                                        "Lead or starring participant in production or events",
                                        "National or international recognition ",
                                        "Lead, starring or critical role for organizations",
                                        "Commercial success and critical acclaim ",
                                        "Significant recognition",
                                        "About the Petitioning Employer",
                                        "Qualifying Employer Relationship",
                                        "Foreign Employer Doing Business",
                                        "US Employer Doing Business",
                                        "Managerial or Executive Position Abroad ",
                                        "Specialized Knowledge",
                                        "Managerial or Executive Offered Position in the US",
                                        "Ability to Pay",
                                        "Offered Position",
                                        "Proof of Specialty Occupation",
                                        "Worksite Information",
                                        "Other"
                                    ]
                                },
                                "expert_quotes": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "expert_quote_analysis": {
                                                "type": "boolean",
                                                "description": "Indicates whether expert letters are quoted or directly integrated into the argument for the criterion."
                                            },
                                            "expert_quote_count": {
                                                "type": "integer",
                                                "description": "Number of expert quotes or excerpts from expert letters that are integrated or directly cited in support of the argument within the AAO decision."
                                            },
                                            "expert_quote_context": {
                                                "type": "string",
                                                "description": "Describes the AAO's commentary, if any, on the quoted expert letters. Possible patterns include: -AAO finds the quotes unpersuasive, conclusory, or lacking in detail. -AAO agrees with and validates the expert's assessment. -No comment from AAO on the expert quotes."
                                            }
                                        }
                                    },
                                    "description": "Letters of support or evidence provided in the case ",
                                    "display_name": "Relevant Letters"
                                },
                                "NIW_criteria": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "description": "NIW criteria (if applicable ), Criteria from Advanced Degree & Exceptional Ability, Prong 1, Prong 2, etc."
                                    }
                                },
                                "context": {
                                    "type": "string",
                                    "description": "Context or relevance of the criteria (e.g., 'demonstrated by evidence provided')."
                                },
                                "outcome": {
                                    "type": "string",
                                    "description": "Outcome of the specific criteria (e.g., 'met', 'not met', 'partially met')."
                                }
                            }
                        },
                        "description": "Specific Criteria Argued (The specific arguments or points raised by the petitioner in the decision)",
                        "display_name": "Specific Criteria Argued"
                    },
                    "applicant_arguments": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": [
                                "Legal",
                                "Procedural",
                                "Factual",
                                "Evidentiary",
                                "Discretionary",
                                "Precedent-Based",
                                "Policy-Based",
                                "Statutory",
                                "Regulatory",
                                "Constitutional",
                                "Equitable",
                                "Public Interest",
                                "Other/NA"
                            ]
                        },
                        "description": "Types of arguments presented by the applicant in support of their appeal.",
                        "display_name": "Applicant Arguments"
                    },
                    "uscis_center": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": [
                                    "Service Center",
                                    "Field Office",
                                    "National Benefits Center",
                                    "International Office"
                                ],
                                "display_name": "USCIS Center Type"
                            },
                            "region": {
                                "type": "string",
                                "description": "Region (e.g., California, Texas, Vermont)",
                                "display_name": "USCIS Center Region"
                            }
                        },
                        "description": "USCIS Center where the case was adjudicated.",
                        "display_name": "USCIS Center"
                    },
                    "number_of_filings": {
                        "type": "integer",
                        "description": "How many appeals and motions were filed in this case",
                        "display_name": "Number of Filings"
                    },
                    "type_of_adjucation": {
                        "type": "string",
                        "enum": [
                            "Appeal",
                            "Motion to Reopen",
                            "Motion to Reconsider",
                            "Combined Motions",
                            "Other/NA"
                        ],
                        "display_name": "Type of Appeal"
                    },
                    "RFE_issued": {
                        "type": "boolean",
                        "description": "True if an RFE was issued, False otherwise",
                        "display_name": "RFE issued"
                    },
                    "NOID_issued": {
                        "type": "boolean",
                        "description": "True if an NOID was issued, False otherwise",
                        "display_name": "NOID issued"
                    },
                    "NOID_factors": {
                        "type": "string",
                        "description": "High-level description of what caused the NOID",
                        "display_name": "NOID factors"
                    },
                    "NOID_response_shortcomings": {
                        "type": "string",
                        "description": "If applicable, shortcomings of the subsequent beneficiary NOID response, leading to a denial",
                        "display_name": "NOID beneficiary response shortcoming"
                    },
                    "summary": {
                        "type": "string",
                        "description": "A generalized summary of the case, including key points and outcomes, must be as short and concise as possible while still being informative",
                        "display_name": "Summary"
                    }
                }
            }
        }
    ],
    "combined_outputs": [
        {
            "url": "https://www.uscis.gov/sites/default/files/err/E2%20-%20Applications%20for%20Certification%20of%20Citizenship/Decisions_Issued_in_2025/JAN312025_02E2309.pdf",
            "json": {
                "type_of_visa_petition": {
                    "visa_type": "Application for Citizenship and Issuance of Certificate Under Section 322",
                    "Form_Type": "Form N-600K"
                },
                "USCIS_decision": {
                    "decision_type": "Denied (Merits)",
                    "specific_reason": "Applicant did not meet the legal and physical custody requirements in section 322 of the Act.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "AAO_decision": {
                    "outcome": "Dismissed",
                    "decision_date": "2025-01-31",
                    "specific_reason": "Applicant did not establish that she is living in the legal and physical custody of her father as required under section 322 of the Act.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "petitioner_type": "Individual",
                "nationalities": [
                    "Eritrea"
                ],
                "legal_citations": [
                    {
                        "text": "8 U.S.C. § 1433",
                        "context": "Section 322 of the Immigration and Nationality Act"
                    },
                    {
                        "text": "8 C.F.R. § 103.3",
                        "context": "Appeal process"
                    },
                    {
                        "text": "Matter of Chawathe, 25 I&N Dec. 369, 375-76 (AAO 2010)",
                        "context": "Burden of proof to demonstrate eligibility by a preponderance of the evidence"
                    },
                    {
                        "text": "Matter of Christo's, Inc., 26 I&N Dec. 537, 537 n.2 (AAO 2015)",
                        "context": "De novo review"
                    },
                    {
                        "text": "Matter of Baires-Larios, 24 I&N Dec. 467, 468 (BIA 2008)",
                        "context": "Burden of establishing claim to U.S. citizenship by a preponderance of credible evidence"
                    },
                    {
                        "text": "Child Citizenship Act of 2000, Pub. L. No. 106-395, 114 Stat. 1631 (Oct. 30, 2000)",
                        "context": "Amendment to Section 322 of the Act"
                    },
                    {
                        "text": "Bagot v. Ashcroft, 398 F.3d 252, 267 (3d Cir. 2005)",
                        "context": "Meaning of 'physical custody' in the context of 'actual uncontested custody'"
                    },
                    {
                        "text": "Matter of M-, 3 I&N Dec. 850, 856 (BIA 1950)",
                        "context": "Interpretation of 'actual uncontested custody'"
                    },
                    {
                        "text": "Section 101(a)(33) of the Act, 8 U.S.C. § 1101(a)(33)",
                        "context": "Definition of 'residence'"
                    },
                    {
                        "text": "INS v. Bagamasbad, 429 U.S. 24, 25 (1976)",
                        "context": "Agencies are not required to make 'purely advisory findings' on issues unnecessary to the ultimate decision"
                    }
                ],
                "specific_criteria_argued": [
                    {
                        "criteria": "Proof of Specialty Occupation",
                        "context": "DNA test to establish biological relationship",
                        "outcome": "met"
                    }
                ],
                "applicant_arguments": [
                    "Factual"
                ],
                "uscis_center": {
                    "type": "Field Office",
                    "region": "Columbus, Ohio"
                },
                "number_of_filings": 1,
                "type_of_adjucation": "Appeal",
                "summary": "The appeal for the Form N-600K, Application for Citizenship and Issuance of Certificate Under Section 322, was dismissed. The applicant did not meet the legal and physical custody requirements as she did not reside with her U.S. citizen father."
            }
        },
        {
            "url": "https://www.uscis.gov/sites/default/files/err/C6%20-%20Dependent%20of%20Juvenile%20Court/Decisions_Issued_in_2025/FEB072025_01C6101.pdf",
            "json": {
                "type_of_visa_petition": {
                    "visa_type": "Special Immigrant Juvenile",
                    "Form_Type": "Form I-360"
                },
                "USCIS_decision": {
                    "decision_type": "Denied (Merits)",
                    "specific_reason": "The Petitioner did not provide a juvenile court order with the required judicial determinations in support of the SIJ classification.",
                    "categorical_reason": "Insufficient Evidence"
                },
                "AAO_decision": {
                    "outcome": "Dismissed",
                    "decision_date": "2025-02-07",
                    "specific_reason": "The Petitioner did not establish by a preponderance of the evidence that the District Court determined that reunification with one or both parents was not viable due to abuse, neglect, abandonment, or a similar basis under state law. Additionally, the District Court did not make a specific finding that it was not in the Petitioner's best interest to be returned to Honduras.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "petitioner_type": "Individual",
                "nationalities": [
                    "Honduras"
                ],
                "legal_citations": [
                    {
                        "text": "8 U.S.C. §§ 1101(a)(27)(J) and 1154(a)(1)(G)",
                        "context": "SIJ classification protects foreign-born children in the United States who cannot reunify with one or both parents because of abuse, neglect, abandonment, or a similar basis under state law."
                    },
                    {
                        "text": "8 C.F.R. § 204.11(b)",
                        "context": "To establish eligibility for SIJ classification, petitioners must show that they are unmarried, under 21 years old, and have been subject to a state juvenile court order determining that they cannot reunify with one or both parents due to abuse, neglect, abandonment, or a similar basis under state law."
                    },
                    {
                        "text": "8 C.F.R. § 204.11(b)(5)",
                        "context": "SIJ classification may only be granted upon the consent of the Secretary of the Department of Homeland Security (DHS), through USCIS, when the petitioner meets all other eligibility criteria and establishes that the request for SIJ classification is bona fide."
                    },
                    {
                        "text": "8 C.F.R. § 204.11(d)(4)",
                        "context": "Where a juvenile court finds that parental reunification is not viable due to a similar basis, such as the death of a parent, the Petitioner must establish that the nature and elements of the state law are indeed similar to the nature and elements of laws on abuse, neglect, or abandonment."
                    },
                    {
                        "text": "8 C.F.R. § 204.11(c)(1)(ii)",
                        "context": "The record must contain evidence of a judicial determination that the juvenile was subjected to such maltreatment by one or both parents under state law."
                    },
                    {
                        "text": "8 C.F.R. § 204.11(c)(3)",
                        "context": "The Petitioner bears the burden of proof to establish eligibility, which includes demonstrating the state law the juvenile court applied in its reunification determination."
                    },
                    {
                        "text": "8 C.F.R. § 204.11(b)(5)",
                        "context": "To warrant USCIS' consent, juveniles must establish that the request for SIJ classification was bona fide, such that a primary reason the requisite juvenile court or administrative determinations were sought was to gain relief from parental abuse, neglect, abandonment, or a similar basis under state law."
                    },
                    {
                        "text": "8 C.F.R. § 204.11(d)(5)(ii)",
                        "context": "The District Court declared that 'the adoption was in the best interests of the child,' without a finding of parental maltreatment; and the Order did not otherwise satisfy the requirements."
                    }
                ],
                "precedent_citations": [
                    {
                        "case_name": "Matter of Chawathe",
                        "context": "The Petitioner bears the burden of proof to demonstrate eligibility by a preponderance of the evidence."
                    },
                    {
                        "case_name": "Matter of Christo's, Inc.",
                        "context": "We review the questions in this matter de novo."
                    },
                    {
                        "case_name": "Budhathoki v. Nielsen",
                        "context": "Whether a state court order submitted to a federal agency for the purpose of gaining a federal benefit made the necessary rulings very much is a question of federal law, not state law, and the agency had authority to examine the orders for that purpose."
                    }
                ],
                "visa_requirements": [
                    "Unmarried",
                    "Under 21 years old",
                    "Subject to a state juvenile court order determining that they cannot reunify with one or both parents due to abuse, neglect, abandonment, or a similar basis under state law",
                    "Judicial determination that it is not in the juvenile's best interest to be returned to their country of nationality or habitual residence"
                ],
                "specific_criteria_argued": [
                    {
                        "criteria": "Information about area of expertise",
                        "context": "The Petitioner argued that the Order found that reunification with his biological parents was not viable due to abandonment and that the factual basis for this determination was based on the affidavit of voluntary relinquishment of parental rights signed by the Petitioner's biological mother, and testimony about his father's death.",
                        "outcome": "not met"
                    },
                    {
                        "criteria": "Information about area of expertise",
                        "context": "The Petitioner argued that the adoption evaluation mentioned that the adoptive parents were 'aware it would not be safe for them to return to Honduras,' and it also mentioned that the Petitioner's father was a hit man in Honduras who was captured by a rival cartel, brutally tortured and then beheaded on social media.",
                        "outcome": "not met"
                    }
                ],
                "applicant_arguments": [
                    "Factual",
                    "Evidentiary"
                ],
                "uscis_center": {
                    "type": "National Benefits Center"
                },
                "number_of_filings": 1,
                "type_of_adjucation": "Appeal",
                "RFE_issued": true,
                "summary": "The Petitioner, a native and citizen of Honduras, sought SIJ classification but was denied due to insufficient evidence of a juvenile court order with the required judicial determinations. The AAO dismissed the appeal, concluding that the Petitioner did not meet the eligibility criteria for SIJ classification."
            }
        },
        {
            "url": "https://www.uscis.gov/sites/default/files/err/C1%20-%20Immigrant%20Religious%20Workers/Decisions_Issued_in_2025/FEB072025_01C1101.pdf",
            "json": {
                "type_of_visa_petition": {
                    "visa_type": "Special Immigrant Religious Worker",
                    "Form_Type": "Form I-360"
                },
                "USCIS_decision": {
                    "decision_type": "Denied (Merits)",
                    "specific_reason": "The Petitioner had not submitted a currently valid determination letter from the IRS confirming its tax-exempt status, had not established that the proposed position would be full-time, and had not shown that the Beneficiary had been continuously employed in a full-time, compensated religious worker position in the two years immediately preceding the filing of the petition.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "AAO_decision": {
                    "outcome": "Dismissed",
                    "decision_date": "2025-02-07",
                    "specific_reason": "The Petitioner did not provide sufficient evidence to establish eligibility at the time of filing, including a valid IRS determination letter, proof of full-time employment, and continuous employment in a compensated religious worker position for the two years preceding the petition.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "petitioner_type": "Church",
                "job_position": {
                    "job_title": "Senior Pastor",
                    "industry": "Religious Services"
                },
                "nationalities": [
                    "N/A"
                ],
                "legal_citations": [
                    {
                        "text": "8 U.S.C. § 1153(b)(4)",
                        "context": "Immigration and Nationality Act section 203(b)(4) providing classification to qualified special immigrant religious workers."
                    },
                    {
                        "text": "8 C.F.R. § 103.3",
                        "context": "Appeal process for the decision."
                    },
                    {
                        "text": "8 C.F.R. §§ 204.5(m)(4), (11)",
                        "context": "Requirements for continuous religious work experience and compensation."
                    },
                    {
                        "text": "8 C.F.R. §§ 204.5(m)(7), (10)",
                        "context": "Requirements for demonstrating ability and intention to compensate the alien."
                    },
                    {
                        "text": "8 C.F.R. §§ 204.5(m)(3), (5), (8)",
                        "context": "Requirements for the religious organization to be tax-exempt."
                    },
                    {
                        "text": "8 C.F.R. § 204.5(m)(8)(iii)(A)",
                        "context": "Requirement for a currently valid IRS determination letter."
                    },
                    {
                        "text": "8 C.F.R. § 103.2(b)(11)",
                        "context": "Requirement for all requested evidence to be submitted together at one time."
                    },
                    {
                        "text": "Matter of Soriano, 19 I&N Dec. 764, 766 (BIA 1988)",
                        "context": "Declining to consider new evidence submitted on appeal."
                    },
                    {
                        "text": "8 C.F.R. §§ 103.2(b)(1), (12)",
                        "context": "Eligibility must be established at the time of filing."
                    },
                    {
                        "text": "Matter of Katigbak, 14 I&N Dec. 45, 49 (Reg'l Comm'r 1971)",
                        "context": "A petition cannot be approved at a future date after the petitioner becomes eligible under a new set of facts."
                    },
                    {
                        "text": "Matter of Izummi, 22 I&N Dec. 169, 175 (Comm'r 1998)",
                        "context": "Eligibility must be established at the time of filing."
                    },
                    {
                        "text": "INS v. Bagamasbad, 429 U.S. 24, 25 (1976)",
                        "context": "Agencies are not required to make purely advisory findings on issues that are unnecessary to the ultimate decision."
                    }
                ],
                "visa_requirements": [
                    "Membership in a religious denomination",
                    "Continuous religious work experience for at least the two-year period before the petition filing date",
                    "Full-time, compensated religious work",
                    "Valid IRS determination letter confirming tax-exempt status",
                    "Ability and intention to compensate the alien"
                ],
                "specific_criteria_argued": [
                    {
                        "criteria": "Employer Documents",
                        "context": "The Petitioner submitted a copy of the form it submitted to the IRS requesting verification of its tax-exempt status and a filing receipt for this form.",
                        "outcome": "not met"
                    },
                    {
                        "criteria": "Employment in critical capacity",
                        "context": "The Petitioner submitted a signed statement indicating that the Beneficiary had been acting as senior pastor for the church since 2012.",
                        "outcome": "not met"
                    },
                    {
                        "criteria": "Ability to Pay",
                        "context": "The Petitioner submitted direct deposit receipts purporting to show payments from the Petitioner to the Beneficiary in the months of August through November 2024.",
                        "outcome": "not met"
                    }
                ],
                "applicant_arguments": [
                    "Evidentiary"
                ],
                "uscis_center": {
                    "type": "Service Center",
                    "region": "California"
                },
                "number_of_filings": 1,
                "type_of_adjucation": "Appeal",
                "RFE_issued": false,
                "NOID_issued": true,
                "NOID_factors": "Insufficient evidence of tax-exempt status, full-time employment, and continuous employment in a compensated religious worker position.",
                "NOID_response_shortcomings": "The Petitioner did not provide sufficient evidence to establish eligibility at the time of filing.",
                "summary": "The Petitioner, a church, sought to classify the Beneficiary as a special immigrant religious worker to perform services as a Senior Pastor. The petition was denied due to insufficient evidence of tax-exempt status, full-time employment, and continuous employment in a compensated religious worker position. The appeal was dismissed as the Petitioner did not provide sufficient evidence to establish eligibility at the time of filing."
            }
        },
        {
            "url": "https://www.uscis.gov/sites/default/files/err/D2%20-%20Temporary%20Worker%20in%20a%20Specialty%20Occupation%20or%20Fashion%20Model%20%28H-1B%29/Decisions_Issued_in_2025/JAN302025_01D2101.pdf",
            "json": {
                "type_of_visa_petition": {
                    "visa_type": "H-1B",
                    "Form_Type": "Form I-129"
                },
                "USCIS_decision": {
                    "decision_type": "Revoked (Post-Approval)",
                    "specific_reason": "The Petitioner violated statutory or regulatory requirements as proscribed by 8 C.F.R. § 214.2(h)(iii)(A)(4) because it did not rebut the evidence that showed that it worked with another entity to unfairly increase the chances of the Beneficiary's selection in the H-1B registration process.",
                    "categorical_reason": "Fraud or Misrepresentation"
                },
                "AAO_decision": {
                    "outcome": "Remanded",
                    "decision_date": "2025-01-30",
                    "specific_reason": "The Director did not sufficiently articulate the finding of fraud based upon the revocation ground.",
                    "categorical_reason": "Procedural Error by USCIS"
                },
                "petitioner_type": "Company",
                "job_position": {
                    "job_title": "Systems Engineer",
                    "industry": "Technology"
                },
                "legal_citations": [
                    {
                        "text": "8 CFR § 214.2(h)(iii)(A)(4)",
                        "context": "The Petitioner violated statutory or regulatory requirements because it did not rebut the evidence that showed that it worked with another entity to unfairly increase the chances of the Beneficiary's selection in the H-1B registration process."
                    },
                    {
                        "text": "8 CFR § 103.3",
                        "context": "The matter is now before us on appeal pursuant to this regulation."
                    },
                    {
                        "text": "8 CFR § 214.2(h)(8)(iii)(A)(i)",
                        "context": "To ensure a fair and equitable allocation of the available H-1B visas in any given fiscal year, USCIS has instituted the registration requirement contained in this regulation."
                    },
                    {
                        "text": "8 CFR § 214.2(h)(11)(iii)",
                        "context": "USCIS may revoke the approval of an H-1B petition pursuant to this regulation."
                    },
                    {
                        "text": "8 CFR § 214.2(h)(11)(iii)(B)",
                        "context": "The regulations require that USCIS provide notice consisting of a detailed statement of the grounds for revocation of the petition approval and provide an opportunity for the petitioner to respond to the notice of intent to revoke."
                    },
                    {
                        "text": "Matter of Chawathe, 25 I&N Dec. 369, 375-76 (AAO 2010)",
                        "context": "The Petitioner bears the burden of proof to demonstrate eligibility by a preponderance of the evidence."
                    },
                    {
                        "text": "Matter of Christa's, Inc., 26 I&N Dec. 537, 537 n.2 (AAO 2015)",
                        "context": "We review the questions in this matter de novo."
                    },
                    {
                        "text": "Matter of Kai Hing Hui, 15 I&N Dec. 288, 289-90 (BIA 1975)",
                        "context": "A material misrepresentation requires that an individual willfully make a material misstatement to a government official for the purpose of obtaining an immigration benefit to which one is not entitled."
                    },
                    {
                        "text": "Matter of Tijam, 22 I&N Dec. 408, 425 (BIA 1998); Matter of Healy and Goodchild, 17 I&N Dec. 22, 28 (BIA 1979)",
                        "context": "The term 'willfully' means knowing and intentionally, as distinguished from accidentally, inadvertently, or in an honest belief that the facts are otherwise."
                    },
                    {
                        "text": "Matter of Ng, 17 I&N Dec. 536, 537 (BIA 1980)",
                        "context": "To be considered material, the misrepresentation must be one which 'tends to shut off a line of inquiry which is relevant to the foreign national's eligibility, and which might well have resulted in a proper determination that he be excluded.'"
                    },
                    {
                        "text": "Matter of M-, 6 I&N Dec. 149 (BIA 1954); Matter of L-L-, 9 I&N Dec. 324 (BIA 1961); Matter of Kai Hing Hui, 15 I&N Dec. at 289-90",
                        "context": "For an immigration officer to find a willful and material misrepresentation in visa petition proceedings, he or she must determine: 1) that the petitioner or beneficiary made a false representation to an authorized official of the United States government; 2) that the misrepresentation was willfully made; and 3) that the fact misrepresented was material."
                    }
                ],
                "precedent_citations": [],
                "visa_requirements": [
                    "Theoretical and practical application of a body of highly specialized knowledge",
                    "Attainment of a bachelor's or higher degree in the specific specialty (or its equivalent) as a minimum prerequisite for entry into the position"
                ],
                "specific_criteria_argued": [
                    {
                        "criteria": "Employer Documents",
                        "context": "The Petitioner asserted that both it and the related entity have legitimate business needs for the systems engineer position that was offered to the Beneficiary and was the basis for the multiple H-1B registrations.",
                        "outcome": "not met"
                    }
                ],
                "applicant_arguments": [
                    "Legal",
                    "Procedural",
                    "Factual",
                    "Evidentiary"
                ],
                "uscis_center": {
                    "type": "Service Center",
                    "region": "California"
                },
                "number_of_filings": 1,
                "type_of_adjucation": "Appeal",
                "RFE_issued": false,
                "NOID_issued": true,
                "NOID_factors": "The Petitioner worked with another entity to submit multiple H-1B registrations to unfairly increase the chances of selection for the Beneficiary.",
                "NOID_response_shortcomings": "The Petitioner did not provide any evidence to support its claim that both it and the related entity submitted their H-1B registrations based upon separate, legitimate business needs.",
                "summary": "The Petitioner, a company, sought to employ the Beneficiary as a Systems Engineer under the H-1B visa. The initial petition was approved but later revoked by the California Service Center due to findings of fraud, specifically that the Petitioner worked with another entity to unfairly increase the chances of the Beneficiary's selection in the H-1B registration process. The AAO remanded the case, withdrawing the Director's finding of fraud due to insufficient articulation but upheld the revocation of the petition."
            }
        },
        {
            "url": "https://www.uscis.gov/sites/default/files/err/B7%20-%20Immigrant%20Petition%20by%20Alien%20Entrepreneur%2C%20Sec.%20203%28b%29%285%29%20of%20the%20INA/Decisions_Issued_in_2025/JAN152025_03B7203.pdf",
            "json": {
                "type_of_visa_petition": {
                    "visa_type": "EB-5 Immigrant Investor",
                    "Form_Type": "Form I-526"
                },
                "USCIS_decision": {
                    "decision_type": "Denied (Merits)",
                    "specific_reason": "The Petitioner did not establish that: (1) he invested or was in the process of investing the required amount of capital in the NCE at the time of filing; (2) the funds he invested in the NCE were derived from a lawful source; and (3) his investment in the NCE created or would likely create at least 10 full-time positions for qualifying employees.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "AAO_decision": {
                    "outcome": "Dismissed",
                    "decision_date": "2025-01-15",
                    "specific_reason": "The Petitioner has not established by a preponderance of the evidence that he is eligible for the visa classification sought. The business plan is neither credible nor comprehensive, and the project has not met established timelines or secured necessary financing.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "petitioner_type": "Individual",
                "job_position": {
                    "job_title": "N/A",
                    "industry": "N/A",
                    "SOC_code": "N/A"
                },
                "positive_factors": [],
                "negative_factors": [],
                "nationalities": [],
                "legal_citations": [
                    {
                        "text": "8 CFR § 204.6(i)(4)(i)",
                        "context": "A petitioner must establish that their investment of the required amount of capital in an NCE will create full-time positions for at least 10 qualifying employees within two years."
                    },
                    {
                        "text": "8 U.S.C. § 1153(b)(5)(A)(ii)",
                        "context": "The investment of the required amount of capital in the NCE must create at least 10 full-time positions for qualifying employees within two years."
                    },
                    {
                        "text": "Matter of Ho, 22 I&N Dec. 206, 213 (Assoc. Comm'r 1998)",
                        "context": "A comprehensive business plan must be sufficiently detailed to permit USCIS to draw reasonable inferences about job-creation potential."
                    },
                    {
                        "text": "Matter of Chawathe, 25 I&N Dec. 369, 375-76 (AAO 2010)",
                        "context": "The Petitioner bears the burden of proof to demonstrate eligibility by a preponderance of the evidence."
                    },
                    {
                        "text": "Matter of Christa's, Inc., 26 I&N Dec. 537, 537 n.2 (AAO 2015)",
                        "context": "We review the questions in this matter de novo."
                    },
                    {
                        "text": "Kungys v. United States, 485 U.S. 759, 770-72 (1988)",
                        "context": "A change is material if it would have a natural tendency to influence or is predictably capable of affecting the decision."
                    },
                    {
                        "text": "INS v. Bagamasbad, 429 U.S. 24, 25 (1976)",
                        "context": "Agencies are not required to make 'purely advisory findings' on issues that are unnecessary to the ultimate decision."
                    }
                ],
                "precedent_citations": [],
                "visa_requirements": [
                    "Investment of the required amount of capital in a new commercial enterprise (NCE).",
                    "Creation of at least 10 full-time positions for qualifying employees within two years.",
                    "Funds invested must be derived from a lawful source."
                ],
                "specific_criteria_argued": [
                    {
                        "criteria": "Comprehensive Business Plan",
                        "context": "The business plan must be credible and demonstrate job creation within two years.",
                        "outcome": "not met"
                    },
                    {
                        "criteria": "Secured Financing",
                        "context": "The project must have secured necessary financing to be credible.",
                        "outcome": "not met"
                    }
                ],
                "applicant_arguments": [
                    "Factual",
                    "Evidentiary",
                    "Regulatory",
                    "Constitutional"
                ],
                "uscis_center": {
                    "type": "Service Center",
                    "region": "Immigrant Investor Program Office"
                },
                "number_of_filings": 1,
                "type_of_adjucation": "Appeal",
                "RFE_issued": true,
                "NOID_issued": true,
                "NOID_factors": "Insufficient evidence to demonstrate that the requisite number of jobs will be created using reasonable methodologies.",
                "NOID_response_shortcomings": "The Petitioner did not provide sufficient evidence to support the capital stack and timeline.",
                "summary": "The Petitioner, seeking EB-5 classification, failed to demonstrate that he invested the required amount of capital in a new commercial enterprise (NCE), that the funds were from a lawful source, and that the investment would create at least 10 full-time positions for qualifying employees. The AAO dismissed the appeal, citing the lack of a credible and comprehensive business plan and the project's failure to meet established timelines or secure necessary financing."
            }
        },
        {
            "url": "https://www.uscis.gov/sites/default/files/err/D14%20-%20Application%20for%20U%20Nonimmigrant%20Status/Decisions_Issued_in_2025/JAN232025_01D14101.pdf",
            "json": {
                "type_of_visa_petition": {
                    "visa_type": "U-1 nonimmigrant classification",
                    "Form_Type": "Form I-918"
                },
                "USCIS_decision": {
                    "decision_type": "Denied (Merits)",
                    "specific_reason": "The Petitioner did not establish eligibility for the benefit sought.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "AAO_decision": {
                    "outcome": "Remanded",
                    "decision_date": "2025-01-23",
                    "specific_reason": "The matter is remanded to the Director for reconsideration of the Applicant's eligibility for U nonimmigrant status.",
                    "categorical_reason": "Other/NA"
                },
                "uscis_center": {
                    "type": "Service Center",
                    "region": "Vermont"
                },
                "summary": "The Petitioner sought U-1 nonimmigrant classification as a victim of qualifying criminal activity. The Vermont Service Center denied the petition, concluding that the Petitioner did not establish eligibility. Upon appeal, the AAO remanded the matter to the Director for reconsideration."
            }
        },
        {
            "url": "https://www.uscis.gov/sites/default/files/err/B5%20-%20Members%20of%20the%20Professions%20holding%20Advanced%20Degrees%20or%20Aliens%20of%20Exceptional%20Ability/Decisions_Issued_in_2025/JAN132025_01B5203.pdf",
            "json": {
                "type_of_visa_petition": {
                    "visa_type": "EB-2 (National Interest Waiver)",
                    "Form_Type": "Form I-140"
                },
                "USCIS_decision": {
                    "decision_type": "Denied (Merits)",
                    "specific_reason": "The record did not establish the Petitioner's eligibility for the requested EB-2 classification or a national interest waiver.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "AAO_decision": {
                    "outcome": "Dismissed",
                    "decision_date": "2025-01-13",
                    "specific_reason": "The Petitioner did not submit new evidence or new facts that establish eligibility for the requested benefit, nor did the Petitioner identify any error of law or policy in our prior decision.",
                    "categorical_reason": "Failure to Meet Motion Requirements"
                },
                "petitioner_type": "Individual",
                "job_position": {
                    "job_title": "Restaurant Manager",
                    "industry": "Hospitality"
                },
                "legal_citations": [
                    {
                        "text": "8 C.F.R. § 103.5(a)(2)",
                        "context": "A motion to reopen must state new facts and be supported by documentary evidence."
                    },
                    {
                        "text": "8 C.F.R. § 103.5(a)(3)",
                        "context": "A motion to reconsider must establish that our prior decision was based on an incorrect application of law or policy and that the decision was incorrect based on the evidence in the record of proceedings at the time of the decision."
                    },
                    {
                        "text": "8 C.F.R. § 103.5(a)(1)(ii)",
                        "context": "Our review on motion is limited to reviewing our latest decision."
                    },
                    {
                        "text": "Matter of Coelho, 20 I&N Dec. 464, 473 (BIA 1992)",
                        "context": "Requiring that new evidence have the potential to change the outcome."
                    },
                    {
                        "text": "Matter of Chawathe, 25 I&N Dec. 369, 375-76 (AAO 2010)",
                        "context": "The Petitioner bears the burden of proof to demonstrate eligibility by a preponderance of the evidence."
                    },
                    {
                        "text": "Matter of O-R-E-, 28 I&N Dec. 330, 336 n.5 (BIA 2021)",
                        "context": "An issue not raised on appeal is waived."
                    },
                    {
                        "text": "INS v. Bagamasbad, 429 U.S. 24, 25 (1976)",
                        "context": "Agencies are not required to make 'purely advisory findings' on issues that are unnecessary to the ultimate decision."
                    },
                    {
                        "text": "Matter of L-A-C-, 26 I&N Dec. 516, 526 n. 7 (BIA 2015)",
                        "context": "Declining to reach alternative issues on appeal where an applicant is otherwise ineligible."
                    },
                    {
                        "text": "Matter of O-S-G-, 24 I&N Dec. 56, 58 (BIA 2006)",
                        "context": "A motion to reconsider is not a process by which a party may submit, in essence, the same brief presented on appeal and seek reconsideration by generally alleging error in the prior Board decision."
                    }
                ],
                "specific_criteria_argued": [
                    {
                        "criteria": "Offered Position",
                        "context": "The Petitioner did not establish eligibility for the underlying EB-2 immigrant classification.",
                        "outcome": "not met"
                    },
                    {
                        "criteria": "Exceptional Ability",
                        "context": "The Petitioner did not meet any of the six evidentiary criteria at 8 C.F.R. § 204.5(k)(3)(ii).",
                        "outcome": "not met"
                    }
                ],
                "applicant_arguments": [
                    "Evidentiary",
                    "Legal"
                ],
                "uscis_center": {
                    "type": "Service Center",
                    "region": "Nebraska"
                },
                "number_of_filings": 3,
                "type_of_adjucation": "Combined Motions",
                "summary": "The Petitioner, a restaurant manager, sought EB-2 classification and a national interest waiver. The Nebraska Service Center denied the petition, and subsequent appeals and motions were dismissed. The AAO dismissed the latest combined motions to reopen and reconsider, citing failure to present new evidence or identify legal errors."
            }
        },
        {
            "url": "https://www.uscis.gov/sites/default/files/err/B2%20-%20Aliens%20with%20Extraordinary%20Ability/Decisions_Issued_in_2025/JAN292025_01B2203.pdf",
            "json": {
                "type_of_visa_petition": {
                    "visa_type": "Immigrant Petition for Alien Workers (Extraordinary Ability)",
                    "Form_Type": "Form I-140"
                },
                "USCIS_decision": {
                    "decision_type": "Denied (Merits)",
                    "specific_reason": "The Petitioner did not establish that he met at least three of the ten initial evidentiary criteria for this immigrant classification.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "AAO_decision": {
                    "outcome": "Dismissed",
                    "decision_date": "2025-01-29",
                    "specific_reason": "The Petitioner did not demonstrate sustained national or international acclaim and is not among the small percentage at the very top of his field.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "petitioner_type": "Individual",
                "job_position": {
                    "job_title": "Data Analytics Leader",
                    "industry": "Technology"
                },
                "specific_criteria_argued": [
                    {
                        "criteria": "Judging the work of others",
                        "context": "The Petitioner participated as a judge of the work of others in his field.",
                        "outcome": "met"
                    },
                    {
                        "criteria": "Lead, starring or critical role for organizations",
                        "context": "The Petitioner served in a leading or critical role for an organization with a distinguished reputation.",
                        "outcome": "met"
                    },
                    {
                        "criteria": "Scholarly Publications",
                        "context": "The Petitioner authored at least one scholarly article in a qualifying publication.",
                        "outcome": "met"
                    }
                ],
                "applicant_arguments": [
                    "Factual",
                    "Evidentiary",
                    "Policy-Based"
                ],
                "uscis_center": {
                    "type": "Service Center",
                    "region": "Nebraska"
                },
                "number_of_filings": 2,
                "type_of_adjucation": "Combined Motions",
                "RFE_issued": false,
                "NOID_issued": false,
                "summary": "The Petitioner, a data analytics leader, sought classification as an individual of extraordinary ability. The Nebraska Service Center denied the petition, concluding the Petitioner did not meet at least three of the ten initial evidentiary criteria. The AAO dismissed the appeal, agreeing that the Petitioner met three criteria but did not demonstrate sustained national or international acclaim. The Petitioner filed combined motions to reopen and reconsider, which were also dismissed."
            }
        },
        {
            "url": "https://www.uscis.gov/sites/default/files/err/A6%20-%20Adjustment%20of%20Alien%20in%20U%20Nonimmigrant%20Status%20I-485%20U%20Sec.%20245%28m%29%281%29%20of%20the%20INA/Decisions_Issued_in_2025/JAN292025_01A6245.pdf",
            "json": {
                "type_of_visa_petition": {
                    "visa_type": "U-2 Nonimmigrant",
                    "Form_Type": "Form I-485"
                },
                "USCIS_decision": {
                    "decision_type": "Denied (Merits)",
                    "specific_reason": "The record did not establish that the applicant was physically present in the United States for a continuous period of at least three years prior to applying for adjustment of status.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "AAO_decision": {
                    "outcome": "Dismissed",
                    "decision_date": "2025-01-29",
                    "specific_reason": "The applicant was absent from the United States for a period exceeding 90 days and did not submit a certification from the law enforcement agency that supported the principal petitioner's U-1 petition certifying that her absence was necessary to assist in the criminal investigation or prosecution. Nor has an official involved in the investigation or prosecution certified that the applicant's absence was otherwise justified.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "petitioner_type": "Individual",
                "nationalities": [
                    "Honduras"
                ],
                "legal_citations": [
                    {
                        "text": "8 CFR § 245.24(a)(1)",
                        "context": "Continuous physical presence is defined as the period of time that an applicant has been physically present in the United States and must be a continuous period of at least 3 years since the date of admission as a U nonimmigrant continuing through the date of the conclusion of adjudication of the U adjustment application."
                    },
                    {
                        "text": "8 CFR § 245.24(b)(3)",
                        "context": "USCIS may in its discretion adjust the status of an individual admitted into the United States as a U nonimmigrant to that of an LPR, if among other requirements, he or she has been physically present in the United States for a continuous period of at least three years since the date of admission as a U nonimmigrant."
                    },
                    {
                        "text": "8 CFR § 103.2(a)(1)",
                        "context": "Every form, benefit request, or document must be submitted and executed in accordance with the form instructions. The form's instructions are hereby incorporated into the regulations requiring its submission."
                    },
                    {
                        "text": "8 CFR § 214.14(d)(1)",
                        "context": "Each applicant for U nonimmigrant status must submit a U petition in accordance with the instructions to the petition."
                    },
                    {
                        "text": "Section 245(m)(2) of the Act",
                        "context": "Absences in excess of 90 days or for any periods in the aggregate exceeding 180 days may be excused if necessary to assist in the investigation or prosecution of the qualifying criminal activity or if an official involved in the investigation or prosecution expressly certifies that the absence was otherwise justified."
                    }
                ],
                "visa_requirements": [
                    "Physically present in the United States for a continuous period of at least three years since the date of admission as a U nonimmigrant."
                ],
                "specific_criteria_argued": [
                    {
                        "criteria": "Other",
                        "context": "The applicant argued that she should not be penalized for the lengthy processing time that forced her to stay in Honduras for more than 180 days.",
                        "outcome": "not met"
                    }
                ],
                "applicant_arguments": [
                    "Legal",
                    "Procedural"
                ],
                "uscis_center": {
                    "type": "Service Center",
                    "region": "Vermont"
                },
                "number_of_filings": 1,
                "type_of_adjucation": "Appeal",
                "RFE_issued": false,
                "NOID_issued": false,
                "summary": "The applicant, a U-2 nonimmigrant, sought to adjust her status to that of a lawful permanent resident. The Vermont Service Center denied her application because she did not meet the continuous physical presence requirement, having been absent from the United States for more than 90 days. The AAO dismissed the appeal, noting that the applicant did not provide the necessary certification from law enforcement to justify her absence."
            }
        },
        {
            "url": "https://www.uscis.gov/sites/default/files/err/B9%20-%20Battered%20Spouse%20or%20Child/Decisions_Issued_in_2025/JAN072025_01B9204.pdf",
            "json": {
                "type_of_visa_petition": {
                    "visa_type": "Petition for Abused Spouse of U.S. Citizen or Lawful Permanent Resident",
                    "Form_Type": "Form I-360"
                },
                "USCIS_decision": {
                    "decision_type": "Denied (Merits)",
                    "specific_reason": "The Petitioner did not establish that she had shared a residence with her spouse or entered into the marriage in good faith.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "AAO_decision": {
                    "outcome": "Dismissed",
                    "decision_date": "2025-01-07",
                    "specific_reason": "The Petitioner did not provide sufficient evidence that she shared a residence with her spouse.",
                    "categorical_reason": "Failure to Meet Eligibility Criteria"
                },
                "petitioner_type": "Individual",
                "nationalities": [
                    "Peru"
                ],
                "legal_citations": [
                    {
                        "text": "8 U.S.C. § 1154(a)(1)(B)(ii)",
                        "context": "VAWA provisions for immigrant classification as an abused spouse of a U.S. citizen."
                    },
                    {
                        "text": "8 C.F.R. § 204.2(c)(1)(ix)",
                        "context": "Petition cannot be approved if the petitioner entered into the marriage to circumvent immigration laws."
                    },
                    {
                        "text": "8 C.F.R. § 204.2(c)(2)(i), (vii)",
                        "context": "Evidence of a good faith marriage."
                    },
                    {
                        "text": "8 U.S.C. § 1101(a)(33)",
                        "context": "Definition of 'residence' for VAWA petitioners."
                    },
                    {
                        "text": "8 C.F.R. § 204.2(c)(1)(v)",
                        "context": "Requirement to show that the petitioner and the abusive spouse resided together."
                    },
                    {
                        "text": "8 C.F.R. § 204.2(c)(2)(i), (iii)",
                        "context": "Evidence showing shared residence."
                    },
                    {
                        "text": "8 C.F.R. § 204.2(c)(2)(i)",
                        "context": "Credibility and weight of evidence for VAWA petitions."
                    },
                    {
                        "text": "8 C.F.R. § 103.3(c)",
                        "context": "Non-precedent decisions do not bind USCIS officers in future adjudications."
                    }
                ],
                "precedent_citations": [
                    {
                        "case_name": "Matter of Chawathe",
                        "context": "Burden of proof to demonstrate eligibility by a preponderance of the evidence."
                    },
                    {
                        "case_name": "Matter of Christa's, Inc.",
                        "context": "De novo review of questions in the matter."
                    },
                    {
                        "case_name": "INS v. Bagamasbad",
                        "context": "Agencies are not required to make findings on issues unnecessary to the results they reach."
                    }
                ],
                "visa_requirements": [
                    "Qualifying relationship as the spouse of a U.S. citizen",
                    "Eligible for immigrant classification based on the qualifying relationship",
                    "Entered into the marriage with the U.S. citizen spouse in good faith",
                    "Battered or subjected to extreme cruelty perpetrated by the petitioner's spouse",
                    "Resided with the spouse"
                ],
                "specific_criteria_argued": [
                    {
                        "criteria": "Affidavits",
                        "context": "Affidavits from individuals with personal knowledge of the relationship.",
                        "outcome": "not met"
                    },
                    {
                        "criteria": "Photographs",
                        "context": "Photographs submitted to demonstrate shared residence and good faith marriage.",
                        "outcome": "not met"
                    },
                    {
                        "criteria": "Text messages",
                        "context": "Snapshots of brief text messages exchanged between the Petitioner and her spouse.",
                        "outcome": "not met"
                    }
                ],
                "applicant_arguments": [
                    "Evidentiary",
                    "Procedural"
                ],
                "uscis_center": {
                    "type": "Service Center",
                    "region": "Vermont"
                },
                "number_of_filings": 1,
                "type_of_adjucation": "Appeal",
                "RFE_issued": true,
                "summary": "The Petitioner, a native and citizen of Peru, sought immigrant classification as an abused spouse of a U.S. citizen under VAWA. The Vermont Service Center denied the petition due to insufficient evidence of shared residence and good faith marriage. The AAO dismissed the appeal, upholding the decision based on the same grounds."
            }
        }
    ]
}"""



# Load the static JSON file
def load_static_json():
    # file_path = "combined_outputs_10_files_20250411_024558.json"
    # with open(file_path, "r", encoding="utf-8") as file:
        # return json.load(static_json)
    pass

# Display schema insights
def display_schema(schema):
    st.subheader("Extraction Functions Schema")
    for function in schema:
        with st.expander(f"Schema: {function['name']}", expanded=False):
            st.write(function["description"])
            st.json(function["parameters"])

# Display combined outputs with all fields
def display_outputs_summary(outputs):
    st.subheader("Combined Outputs Summary")
    st.markdown(f"**Total Cases:** {len(outputs)}")
    for idx, output in enumerate(outputs, start=1):
        case_url = output["url"]
        with st.expander(f"Case {idx}"):
            # Add a button icon to open the case URL in a popup
            st.markdown(
                f'<a href="{case_url}" target="_blank" style="text-decoration: none;">'
                f'<button style="background-color: #4CAF50; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">'
                f'🔗 Preview AAO Decision</button></a>',
                unsafe_allow_html=True,
            )
            st.markdown("### All Fields")
            st.json(output["json"])

# Main Streamlit app
def main():
    st.title("Features Extraction Overview")
    st.markdown("This app provides insights into the schema and data of the static JSON file.")

    # Load JSON data
    data = json.loads(static_json)

    # Display schema insights
    if "extraction_functions_schema" in data:
        display_schema(data["extraction_functions_schema"])

    # Display combined outputs summary
    if "combined_outputs" in data:
        display_outputs_summary(data["combined_outputs"])
    else:
        st.warning("No combined outputs found in the JSON file.")

if __name__ == "__main__":
    main()
