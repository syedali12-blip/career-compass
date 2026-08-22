"""
Career Compass — Curated Pakistani university reference data

WHY CURATED, NOT LIVE: HEC (Higher Education Commission) publishes official
rankings, but not via any public API — and their most recent ranking cycle
is already a few years old by the time it's published (a known limitation
of HEC's own process, not something we can fix). There's also no live API
for tuition fees, which change yearly per institution. This file is a
manually maintained reference table, to be disclosed transparently as such
in the research paper — same honesty principle as the companies/courses data.

Fee figures are APPROXIMATE ANNUAL RANGES in PKR, based on publicly available
information at time of writing, and will drift as universities adjust fees.
These are for general orientation only, not exact quotes.

"admission_competitiveness" is a QUALITATIVE, reputation-based estimate
(Highly Competitive / Competitive / Moderate) — unlike the other fields, this
is NOT backed by an official published acceptance-rate statistic (Pakistani
universities generally don't publish these consistently). It should be
disclosed in the paper as a general estimate, not a hard data point.

SOURCING NOTE: the original 25 entries were built primarily from general
knowledge. A later review (August 2026) added 6 more universities (Habib
University, IoBM, Sukkur IBA, National Textile University, Bahria University,
PIEAS) after cross-checking founding year, sector, and program details
against web search results, since these were flagged as missing by the
project owner. Fee ranges for these newer entries are still approximate
estimates and should be verified against each institution's own published
fee structure before being treated as exact — same limitation as the rest
of this file. Program lists throughout remain non-exhaustive; students
should confirm current offerings on each university's official website.

Last reviewed: August 2026.
"""

UNIVERSITIES = [
    {
        "name": "National University of Sciences and Technology (NUST)",
        "city": "Islamabad", "category": "Engineering", "sector": "Public", "established": 1991,
        "hec_rank": "1 (General, 2023 HEC ranking)",
        "admission_competitiveness": "Highly Competitive",
        "approx_annual_fee_pkr": "450,000 – 700,000",
        "notable_programs": ["Computer Science", "Electrical Engineering", "Mechanical Engineering",
                              "Software Engineering", "Business Administration (NBS)", "Civil Engineering"],
    },
    {
        "name": "Lahore University of Management Sciences (LUMS)",
        "city": "Lahore", "category": "Business", "sector": "Private", "established": 1985,
        "hec_rank": "1 (Business, 2023 HEC ranking)",
        "admission_competitiveness": "Highly Competitive",
        "approx_annual_fee_pkr": "1,100,000 – 1,600,000",
        "notable_programs": ["Business Administration", "Computer Science", "Economics",
                              "Law", "Social Sciences", "Electrical Engineering"],
    },
    {
        "name": "Institute of Business Administration (IBA) Karachi",
        "city": "Karachi", "category": "Business", "sector": "Public", "established": 1955,
        "hec_rank": "2 (Business, 2023 HEC ranking)",
        "admission_competitiveness": "Highly Competitive",
        "approx_annual_fee_pkr": "500,000 – 900,000",
        "notable_programs": ["Business Administration", "Economics", "Computer Science",
                              "Accounting & Finance", "Social Sciences"],
    },
    {
        "name": "FAST National University (FAST-NUCES)",
        "city": "Lahore / Karachi / Islamabad", "category": "Engineering", "sector": "Private", "established": 2000,
        "hec_rank": "Top-tier (Computing, 2023 HEC ranking)",
        "admission_competitiveness": "Competitive",
        "approx_annual_fee_pkr": "350,000 – 550,000",
        "notable_programs": ["Computer Science", "Software Engineering", "Data Science",
                              "Artificial Intelligence", "Cyber Security", "Electrical Engineering"],
    },
    {
        "name": "Ghulam Ishaq Khan Institute (GIKI)",
        "city": "Topi, KP", "category": "Engineering", "sector": "Private", "established": 1993,
        "hec_rank": "Top-tier (Engineering, 2023 HEC ranking)",
        "admission_competitiveness": "Highly Competitive",
        "approx_annual_fee_pkr": "500,000 – 750,000",
        "notable_programs": ["Computer Engineering", "Electrical Engineering", "Mechanical Engineering",
                              "Chemical Engineering", "Materials Science"],
    },
    {
        "name": "University of the Punjab",
        "city": "Lahore", "category": "General", "sector": "Public", "established": 1882,
        "hec_rank": "Top-tier (General, 2023 HEC ranking)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "40,000 – 150,000",
        "notable_programs": ["Law", "Economics", "Physics", "Chemistry", "English Literature", "Sociology"],
    },
    {
        "name": "Quaid-i-Azam University",
        "city": "Islamabad", "category": "General", "sector": "Public", "established": 1967,
        "hec_rank": "Top-tier (General, 2023 HEC ranking)",
        "admission_competitiveness": "Competitive",
        "approx_annual_fee_pkr": "40,000 – 150,000",
        "notable_programs": ["Physics", "International Relations", "Biotechnology",
                              "Economics", "Computer Science"],
    },
    {
        "name": "Aga Khan University",
        "city": "Karachi", "category": "Medical", "sector": "Private", "established": 1983,
        "hec_rank": "1 (Medical, 2023 HEC ranking)",
        "admission_competitiveness": "Highly Competitive",
        "approx_annual_fee_pkr": "1,000,000 – 1,800,000",
        "notable_programs": ["Medicine (MBBS)", "Nursing", "Public Health"],
    },
    {
        "name": "King Edward Medical University",
        "city": "Lahore", "category": "Medical", "sector": "Public", "established": 1860,
        "hec_rank": "Top-tier (Medical, 2023 HEC ranking)",
        "admission_competitiveness": "Highly Competitive",
        "approx_annual_fee_pkr": "50,000 – 200,000",
        "notable_programs": ["Medicine (MBBS)", "Dentistry"],
    },
    {
        "name": "National College of Arts (NCA)",
        "city": "Lahore", "category": "Arts / Design", "sector": "Public", "established": 1875,
        "hec_rank": "Top-tier (Arts, 2023 HEC ranking)",
        "admission_competitiveness": "Competitive",
        "approx_annual_fee_pkr": "150,000 – 350,000",
        "notable_programs": ["Fine Arts", "Architecture", "Graphic Design",
                              "Product Design", "Textile Design"],
    },
    {
        "name": "Indus Valley School of Art and Architecture",
        "city": "Karachi", "category": "Arts / Design", "sector": "Private", "established": 1989,
        "hec_rank": "Recognized (Arts)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "500,000 – 800,000",
        "notable_programs": ["Architecture", "Communication Design", "Textile Design", "Fine Arts"],
    },
    {
        "name": "University of Engineering and Technology (UET) Lahore",
        "city": "Lahore", "category": "Engineering", "sector": "Public", "established": 1921,
        "hec_rank": "Top-tier (Engineering, 2023 HEC ranking)",
        "admission_competitiveness": "Competitive",
        "approx_annual_fee_pkr": "60,000 – 180,000",
        "notable_programs": ["Civil Engineering", "Mechanical Engineering", "Electrical Engineering",
                              "Chemical Engineering", "Computer Science"],
    },
    {
        "name": "NED University of Engineering and Technology",
        "city": "Karachi", "category": "Engineering", "sector": "Public", "established": 1921,
        "hec_rank": "Top-tier (Engineering, 2023 HEC ranking)",
        "admission_competitiveness": "Competitive",
        "approx_annual_fee_pkr": "50,000 – 160,000",
        "notable_programs": ["Civil Engineering", "Computer Science & IT", "Electrical Engineering",
                              "Mechanical Engineering"],
    },
    {
        "name": "Mehran University of Engineering and Technology",
        "city": "Jamshoro, Sindh", "category": "Engineering", "sector": "Public", "established": 1963,
        "hec_rank": "Recognized (Engineering)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "40,000 – 120,000",
        "notable_programs": ["Civil Engineering", "Computer Systems Engineering", "Chemical Engineering"],
    },
    {
        "name": "COMSATS University Islamabad",
        "city": "Islamabad (multi-campus)", "category": "Engineering", "sector": "Public", "established": 1998,
        "hec_rank": "Recognized (Computing/Engineering)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "150,000 – 300,000",
        "notable_programs": ["Computer Science", "Software Engineering", "Electrical Engineering", "Business Administration"],
    },
    {
        "name": "Air University",
        "city": "Islamabad", "category": "Engineering", "sector": "Public", "established": 2002,
        "hec_rank": "Recognized (Engineering/Computing)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "180,000 – 320,000",
        "notable_programs": ["Aerospace Engineering", "Computer Science", "Electrical Engineering"],
    },
    {
        "name": "Institute of Space Technology (IST)",
        "city": "Islamabad", "category": "Engineering", "sector": "Public", "established": 2002,
        "hec_rank": "Recognized (Engineering/Space Sciences)",
        "admission_competitiveness": "Competitive",
        "approx_annual_fee_pkr": "150,000 – 280,000",
        "notable_programs": ["Aerospace Engineering", "Space Science", "Electrical Engineering", "Computer Science"],
    },
    {
        "name": "University of Management and Technology (UMT)",
        "city": "Lahore", "category": "Business", "sector": "Private", "established": 1990,
        "hec_rank": "Recognized (Business/General)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "250,000 – 450,000",
        "notable_programs": ["Business Administration", "Computer Science", "Architecture", "Law"],
    },
    {
        "name": "SZABIST University",
        "city": "Karachi / Islamabad", "category": "Business", "sector": "Private", "established": 1995,
        "hec_rank": "Recognized (Business/Computing)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "300,000 – 500,000",
        "notable_programs": ["Business Administration", "Computer Science", "Media Sciences", "Social Sciences"],
    },
    {
        "name": "Iqra University",
        "city": "Karachi", "category": "Business", "sector": "Private", "established": 1998,
        "hec_rank": "Recognized (Business)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "220,000 – 380,000",
        "notable_programs": ["Business Administration", "Computer Science", "Media Sciences"],
    },
    {
        "name": "University of Central Punjab (UCP)",
        "city": "Lahore", "category": "Business", "sector": "Private", "established": 1999,
        "hec_rank": "Recognized (Business/General)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "200,000 – 400,000",
        "notable_programs": ["Business Administration", "Computer Science", "Law", "Pharmacy"],
    },
    {
        "name": "Dow University of Health Sciences",
        "city": "Karachi", "category": "Medical", "sector": "Public", "established": 1945,
        "hec_rank": "Top-tier (Medical, 2023 HEC ranking)",
        "admission_competitiveness": "Highly Competitive",
        "approx_annual_fee_pkr": "60,000 – 200,000",
        "notable_programs": ["Medicine (MBBS)", "Dentistry", "Pharmacy", "Nursing"],
    },
    {
        "name": "Ziauddin University",
        "city": "Karachi", "category": "Medical", "sector": "Private", "established": 1995,
        "hec_rank": "Recognized (Medical)",
        "admission_competitiveness": "Competitive",
        "approx_annual_fee_pkr": "800,000 – 1,400,000",
        "notable_programs": ["Medicine (MBBS)", "Nursing", "Physical Therapy"],
    },
    {
        "name": "Beaconhouse National University (BNU)",
        "city": "Lahore", "category": "Arts / Design", "sector": "Private", "established": 2003,
        "hec_rank": "Recognized (Arts/Design)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "400,000 – 700,000",
        "notable_programs": ["Architecture", "Media Studies", "Fine Arts", "Liberal Arts"],
    },
    {
        "name": "Forman Christian College (FCC)",
        "city": "Lahore", "category": "General", "sector": "Private", "established": 1864,
        "hec_rank": "Recognized (General)",
        "admission_competitiveness": "Competitive",
        "approx_annual_fee_pkr": "300,000 – 550,000",
        "notable_programs": ["Economics", "Computer Science", "Social Sciences", "Business Administration"],
    },
    {
        "name": "University of Karachi",
        "city": "Karachi", "category": "General", "sector": "Public", "established": 1951,
        "hec_rank": "Recognized (General)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "30,000 – 120,000",
        "notable_programs": ["Economics", "International Relations", "Pharmacy", "Chemistry"],
    },
    {
        "name": "Habib University",
        "city": "Karachi", "category": "General", "sector": "Private", "established": 2010,
        "hec_rank": "Recognized (Liberal Arts & Sciences)",
        "admission_competitiveness": "Highly Competitive",
        "approx_annual_fee_pkr": "1,200,000 – 1,700,000",
        "notable_programs": ["Computer Science", "Electrical Engineering", "Communication Design",
                              "Social Development & Policy", "Comparative Humanities"],
    },
    {
        "name": "Institute of Business Management (IoBM)",
        "city": "Karachi", "category": "Business", "sector": "Private", "established": 1995,
        "hec_rank": "Recognized (Business)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "300,000 – 550,000",
        "notable_programs": ["Business Administration", "Computer Science", "Data Science",
                              "Software Engineering", "Economics", "Electrical Engineering"],
    },
    {
        "name": "Sukkur IBA University",
        "city": "Sukkur, Sindh", "category": "Business", "sector": "Public", "established": 2006,
        "hec_rank": "Recognized (Business)",
        "admission_competitiveness": "Competitive",
        "approx_annual_fee_pkr": "80,000 – 200,000",
        "notable_programs": ["Business Administration", "Computer Science", "Economics", "Accounting & Finance"],
    },
    {
        "name": "National Textile University (NTU)",
        "city": "Faisalabad", "category": "Engineering", "sector": "Public", "established": 1959,
        "hec_rank": "Recognized (Engineering/Textile)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "80,000 – 180,000",
        "notable_programs": ["Textile Engineering", "Textile Design", "Computer Science", "Business Administration"],
    },
    {
        "name": "Bahria University",
        "city": "Islamabad / Karachi / Lahore", "category": "Engineering", "sector": "Public", "established": 2000,
        "hec_rank": "Recognized (Engineering/Computing)",
        "admission_competitiveness": "Moderate",
        "approx_annual_fee_pkr": "180,000 – 350,000",
        "notable_programs": ["Computer Science", "Electrical Engineering", "Business Administration",
                              "Health Sciences (DPT)", "Law", "Artificial Intelligence"],
    },
    {
        "name": "Pakistan Institute of Engineering and Applied Sciences (PIEAS)",
        "city": "Islamabad", "category": "Engineering", "sector": "Public", "established": 1967,
        "hec_rank": "Top-tier (Engineering/Applied Sciences, postgraduate-focused)",
        "admission_competitiveness": "Highly Competitive",
        "approx_annual_fee_pkr": "40,000 – 100,000",
        "notable_programs": ["Nuclear Engineering", "Electrical Engineering", "Computer Science", "Physics"],
    },
]

# Authoritative, hand-ranked top-7 universities per degree program, provided by
# the project owner from a researched top-10 list per degree (trimmed to 7 here).
# This is DIFFERENT from UNIVERSITIES above: that list holds full detail records
# (fees, sector, HEC rank, city...) for ~32 major universities; this dict is a
# curated RANKING across 47 degree programs, some naming universities not in the
# detailed UNIVERSITIES list above. get_top_universities_for_degree() enriches
# each name with a full UNIVERSITIES record where one exists (exact name match)
# and returns a lighter {"name": ...} entry otherwise, so the ranking is never
# silently dropped just because we lack fee/city detail for that institution.
# Order matters: index 0 is the #1-ranked university for that degree.
DEGREE_TOP_UNIVERSITIES = {
    "Accounting & Finance": ["Lahore University of Management Sciences (LUMS)", "Institute of Business Administration (IBA) Karachi", "National University of Sciences and Technology (NUST)", "Institute of Business Management (IoBM)", "Lahore School of Economics", "University of Management and Technology (UMT)", "Iqra University"],
    "Aerospace Engineering": ["National University of Sciences and Technology (NUST)", "Institute of Space Technology (IST)", "Air University", "Pakistan Institute of Engineering and Applied Sciences (PIEAS)", "Ghulam Ishaq Khan Institute (GIKI)", "UET Taxila", "University of Engineering and Technology (UET) Lahore"],
    "Architecture": ["National College of Arts (NCA)", "National University of Sciences and Technology (NUST)", "University of Engineering and Technology (UET) Lahore", "Indus Valley School of Art and Architecture", "University of Karachi", "Dawood University", "Beaconhouse National University (BNU)"],
    "Artificial Intelligence": ["National University of Sciences and Technology (NUST)", "FAST National University (FAST-NUCES)", "COMSATS University Islamabad", "Ghulam Ishaq Khan Institute (GIKI)", "Pakistan Institute of Engineering and Applied Sciences (PIEAS)", "University of Engineering and Technology (UET) Lahore", "Air University"],
    "Biotechnology": ["National University of Sciences and Technology (NUST)", "Quaid-i-Azam University", "COMSATS University Islamabad", "University of Karachi", "University of the Punjab", "UAF", "Ghulam Ishaq Khan Institute (GIKI)"],
    "Business Administration": ["Lahore University of Management Sciences (LUMS)", "Institute of Business Administration (IBA) Karachi", "National University of Sciences and Technology (NUST)", "Lahore School of Economics", "Institute of Business Management (IoBM)", "University of Management and Technology (UMT)", "SZABIST University"],
    "Business Administration (NBS)": ["National University of Sciences and Technology (NUST)", "Lahore University of Management Sciences (LUMS)", "Institute of Business Administration (IBA) Karachi", "Lahore School of Economics", "Institute of Business Management (IoBM)", "University of Management and Technology (UMT)", "SZABIST University"],
    "Chemical Engineering": ["University of Engineering and Technology (UET) Lahore", "National University of Sciences and Technology (NUST)", "University of the Punjab", "UET Peshawar", "Mehran University of Engineering and Technology", "Dawood University", "NED University of Engineering and Technology"],
    "Chemistry": ["Quaid-i-Azam University", "University of the Punjab", "University of Karachi", "COMSATS University Islamabad", "UAF", "National University of Sciences and Technology (NUST)", "GC University Lahore"],
    "Civil Engineering": ["University of Engineering and Technology (UET) Lahore", "National University of Sciences and Technology (NUST)", "NED University of Engineering and Technology", "UET Taxila", "Mehran University of Engineering and Technology", "UET Peshawar", "Ghulam Ishaq Khan Institute (GIKI)"],
    "Communication Design": ["Indus Valley School of Art and Architecture", "National College of Arts (NCA)", "Beaconhouse National University (BNU)", "Karachi School of Art", "University of Karachi", "University of Lahore", "COMSATS University Islamabad"],
    "Comparative Humanities": ["Lahore University of Management Sciences (LUMS)", "Habib University", "Forman Christian College (FCC)", "Quaid-i-Azam University", "University of the Punjab", "University of Karachi", "Beaconhouse National University (BNU)"],
    "Computer Engineering": ["National University of Sciences and Technology (NUST)", "UET Taxila", "FAST National University (FAST-NUCES)", "COMSATS University Islamabad", "University of Engineering and Technology (UET) Lahore", "Ghulam Ishaq Khan Institute (GIKI)", "Air University"],
    "Computer Science": ["National University of Sciences and Technology (NUST)", "FAST National University (FAST-NUCES)", "Lahore University of Management Sciences (LUMS)", "COMSATS University Islamabad", "Ghulam Ishaq Khan Institute (GIKI)", "Pakistan Institute of Engineering and Applied Sciences (PIEAS)", "University of Engineering and Technology (UET) Lahore"],
    "Computer Science & IT": ["National University of Sciences and Technology (NUST)", "FAST National University (FAST-NUCES)", "COMSATS University Islamabad", "Lahore University of Management Sciences (LUMS)", "Ghulam Ishaq Khan Institute (GIKI)", "Information Technology University", "University of Engineering and Technology (UET) Lahore"],
    "Computer Systems Engineering": ["National University of Sciences and Technology (NUST)", "UET Taxila", "Ghulam Ishaq Khan Institute (GIKI)", "FAST National University (FAST-NUCES)", "University of Engineering and Technology (UET) Lahore", "COMSATS University Islamabad", "Air University"],
    "Cyber Security": ["National University of Sciences and Technology (NUST)", "FAST National University (FAST-NUCES)", "Air University", "COMSATS University Islamabad", "Bahria University", "Ghulam Ishaq Khan Institute (GIKI)", "Pakistan Institute of Engineering and Applied Sciences (PIEAS)"],
    "Data Science": ["Lahore University of Management Sciences (LUMS)", "National University of Sciences and Technology (NUST)", "FAST National University (FAST-NUCES)", "COMSATS University Islamabad", "Pakistan Institute of Engineering and Applied Sciences (PIEAS)", "Information Technology University", "Ghulam Ishaq Khan Institute (GIKI)"],
    "Dentistry": ["Aga Khan University", "Dow University of Health Sciences", "King Edward Medical University", "Fatima Jinnah Dental College", "University of Lahore", "Ziauddin University", "Bahria University"],
    "Economics": ["Lahore University of Management Sciences (LUMS)", "Lahore School of Economics", "Quaid-i-Azam University", "Institute of Business Administration (IBA) Karachi", "University of the Punjab", "National University of Sciences and Technology (NUST)", "PIDE"],
    "Electrical Engineering": ["National University of Sciences and Technology (NUST)", "University of Engineering and Technology (UET) Lahore", "Ghulam Ishaq Khan Institute (GIKI)", "Pakistan Institute of Engineering and Applied Sciences (PIEAS)", "FAST National University (FAST-NUCES)", "COMSATS University Islamabad", "UET Taxila"],
    "English Literature": ["Lahore University of Management Sciences (LUMS)", "Forman Christian College (FCC)", "Quaid-i-Azam University", "University of the Punjab", "University of Karachi", "GC University Lahore", "Beaconhouse National University (BNU)"],
    "Fine Arts": ["National College of Arts (NCA)", "Indus Valley School of Art and Architecture", "Beaconhouse National University (BNU)", "University of Karachi", "University of the Punjab", "Karachi School of Art", "University of Peshawar"],
    "Graphic Design": ["Indus Valley School of Art and Architecture", "National College of Arts (NCA)", "Beaconhouse National University (BNU)", "Karachi School of Art", "PIFD", "University of Karachi", "University of Lahore"],
    "Health Sciences (DPT)": ["Aga Khan University", "University of Health Sciences", "University of Lahore", "Ziauddin University", "Dow University of Health Sciences", "Khyber Medical University", "Bahria University"],
    "International Relations": ["Quaid-i-Azam University", "National University of Sciences and Technology (NUST)", "National University of Modern Languages", "University of Karachi", "University of the Punjab", "Bahria University", "COMSATS University Islamabad"],
    "Law": ["Lahore University of Management Sciences (LUMS)", "University of Punjab Law College", "University of Karachi", "University of Peshawar", "Quaid-i-Azam University", "Bahria University", "University of Lahore"],
    "Liberal Arts": ["Habib University", "Lahore University of Management Sciences (LUMS)", "Forman Christian College (FCC)", "Institute of Business Administration (IBA) Karachi", "Beaconhouse National University (BNU)", "National College of Arts (NCA)", "University of Karachi"],
    "Materials Science": ["National University of Sciences and Technology (NUST)", "Pakistan Institute of Engineering and Applied Sciences (PIEAS)", "University of Engineering and Technology (UET) Lahore", "Ghulam Ishaq Khan Institute (GIKI)", "University of the Punjab", "UET Taxila", "NED University of Engineering and Technology"],
    "Mechanical Engineering": ["National University of Sciences and Technology (NUST)", "University of Engineering and Technology (UET) Lahore", "Ghulam Ishaq Khan Institute (GIKI)", "NED University of Engineering and Technology", "UET Taxila", "Pakistan Institute of Engineering and Applied Sciences (PIEAS)", "Mehran University of Engineering and Technology"],
    "Media Sciences": ["SZABIST University", "Beaconhouse National University (BNU)", "University of Karachi", "National University of Modern Languages", "Bahria University", "Iqra University", "University of Lahore"],
    "Media Studies": ["University of Karachi", "SZABIST University", "Beaconhouse National University (BNU)", "National University of Modern Languages", "Bahria University", "Iqra University", "University of the Punjab"],
    "Medicine (MBBS)": ["Aga Khan University", "King Edward Medical University", "Dow University of Health Sciences", "Khyber Medical University", "Fatima Jinnah Medical University", "Allama Iqbal Medical College", "Rawalpindi Medical University"],
    "Nuclear Engineering": ["Pakistan Institute of Engineering and Applied Sciences (PIEAS)", "National University of Sciences and Technology (NUST)", "University of the Punjab", "University of Engineering and Technology (UET) Lahore", "Quaid-i-Azam University", "COMSATS University Islamabad", "Ghulam Ishaq Khan Institute (GIKI)"],
    "Nursing": ["Aga Khan University", "Dow University of Health Sciences", "Shifa Tameer-e-Millat University", "Ziauddin University", "Khyber Medical University", "University of Lahore", "Liaquat University of Medical and Health Sciences"],
    "Pharmacy": ["University of the Punjab", "University of Karachi", "Hamdard University", "COMSATS University Islamabad", "BZU", "University of Lahore", "Riphah International University"],
    "Physical Therapy": ["Aga Khan University", "University of Health Sciences", "Dow University of Health Sciences", "University of Lahore", "Ziauddin University", "Khyber Medical University", "Riphah International University"],
    "Physics": ["Quaid-i-Azam University", "Pakistan Institute of Engineering and Applied Sciences (PIEAS)", "National University of Sciences and Technology (NUST)", "University of the Punjab", "COMSATS University Islamabad", "University of Karachi", "GC University Lahore"],
    "Product Design": ["National College of Arts (NCA)", "Indus Valley School of Art and Architecture", "Beaconhouse National University (BNU)", "PIFD", "National University of Sciences and Technology (NUST)", "University of Lahore", "COMSATS University Islamabad"],
    "Public Health": ["Aga Khan University", "Health Services Academy", "Dow University of Health Sciences", "Khyber Medical University", "University of Health Sciences", "Ziauddin University", "COMSATS University Islamabad"],
    "Social Development & Policy": ["Lahore University of Management Sciences (LUMS)", "Quaid-i-Azam University", "PIDE", "University of Karachi", "University of the Punjab", "COMSATS University Islamabad", "Forman Christian College (FCC)"],
    "Social Sciences": ["Lahore University of Management Sciences (LUMS)", "Quaid-i-Azam University", "University of Karachi", "University of the Punjab", "Forman Christian College (FCC)", "PIDE", "National University of Sciences and Technology (NUST)"],
    "Sociology": ["Quaid-i-Azam University", "University of Karachi", "University of the Punjab", "University of Peshawar", "University of Sindh", "BZU", "GC University Lahore"],
    "Software Engineering": ["FAST National University (FAST-NUCES)", "National University of Sciences and Technology (NUST)", "COMSATS University Islamabad", "Ghulam Ishaq Khan Institute (GIKI)", "University of Engineering and Technology (UET) Lahore", "Bahria University", "Air University"],
    "Space Science": ["Institute of Space Technology (IST)", "National University of Sciences and Technology (NUST)", "Pakistan Institute of Engineering and Applied Sciences (PIEAS)", "University of the Punjab", "Quaid-i-Azam University", "COMSATS University Islamabad", "University of Karachi"],
    "Textile Design": ["National Textile University (NTU)", "PIFD", "National College of Arts (NCA)", "Indus Valley School of Art and Architecture", "Beaconhouse National University (BNU)", "University of Karachi", "University of the Punjab"],
    "Textile Engineering": ["National Textile University (NTU)", "University of Engineering and Technology (UET) Lahore", "University of Faisalabad", "University of the Punjab", "BZU", "NED University of Engineering and Technology", "Mehran University of Engineering and Technology"],
}


CATEGORIES = ["All", "Engineering", "Business", "Medical", "General", "Arts / Design"]


def get_universities(category=None):
    """Returns the curated university list, optionally filtered by category."""
    if not category or category == "All":
        return UNIVERSITIES
    return [u for u in UNIVERSITIES if u["category"] == category]


def get_all_programs():
    """
    Returns a sorted, de-duplicated list of every program name — combining
    both data sources: the 32 detailed universities' notable_programs, AND
    the 47 degrees in DEGREE_TOP_UNIVERSITIES (the authoritative curated
    ranking, which covers more degree programs than notable_programs alone,
    e.g. "Nuclear Engineering", "Space Science", "Public Health").
    """
    programs = set()
    for u in UNIVERSITIES:
        programs.update(u["notable_programs"])
    programs.update(DEGREE_TOP_UNIVERSITIES.keys())
    return sorted(programs)


def get_universities_for_program(program_name):
    """
    Returns universities offering a given program.

    Prefers the authoritative DEGREE_TOP_UNIVERSITIES ranking when the
    program name matches one of the 47 curated degrees exactly — real
    researched ranking data beats the derived proxy below. Falls back to
    ordering by 'Highly Competitive' / higher-tier institutions first
    (a simple proxy for "best university for this degree") when the
    program isn't in the curated degree list.
    """
    if program_name in DEGREE_TOP_UNIVERSITIES:
        return get_top_universities_for_degree(program_name, limit=7)

    competitiveness_order = {"Highly Competitive": 0, "Competitive": 1, "Moderate": 2}
    matches = [u for u in UNIVERSITIES if program_name in u["notable_programs"]]
    return sorted(matches, key=lambda u: competitiveness_order.get(u["admission_competitiveness"], 3))


_UNIVERSITY_BY_NAME = {u["name"]: u for u in UNIVERSITIES}


def _enrich_university_name(name):
    """
    Looks up a name from DEGREE_TOP_UNIVERSITIES against the detailed
    UNIVERSITIES records. Returns the full record if we have one (fees,
    city, HEC rank, etc.), or a minimal {"name": ...} dict if we don't —
    DEGREE_TOP_UNIVERSITIES names ~74 distinct institutions across 47
    degrees, but UNIVERSITIES only holds full detail for ~32 of the
    biggest/most-referenced ones, so this is expected for institutions
    like "Fatima Jinnah Dental College" or "Health Services Academy".
    """
    record = _UNIVERSITY_BY_NAME.get(name)
    if record:
        return dict(record)  # copy, so callers can't mutate the source data
    return {"name": name, "city": None, "category": None, "sector": None,
            "hec_rank": None, "admission_competitiveness": None,
            "approx_annual_fee_pkr": None, "notable_programs": [],
            "detail_available": False}


def get_top_universities_for_degree(degree_name, limit=7):
    """
    Returns the authoritative, hand-ranked top universities for a specific
    degree program (see DEGREE_TOP_UNIVERSITIES above), enriched with full
    detail records where we have them. This is the PREFERRED source when
    the degree name is known exactly — it reflects real researched
    rankings, not a derived proxy like get_universities_for_program().
    Returns [] if the degree isn't in our curated list.
    """
    if not degree_name or degree_name not in DEGREE_TOP_UNIVERSITIES:
        return []
    names = DEGREE_TOP_UNIVERSITIES[degree_name][:limit]
    return [_enrich_university_name(n) for n in names]


def find_matching_degree(text):
    """
    Fuzzy-matches free text (an O*NET occupation title, a dream_field
    answer, an interest label) against the 47 curated degree names in
    DEGREE_TOP_UNIVERSITIES. Tries exact match first, then substring
    containment in either direction. Returns the matched degree name, or
    None if nothing reasonably matches — callers should fall back to the
    broader category-based logic in that case, not force a bad match.
    """
    if not text:
        return None
    text_lower = text.lower().strip()

    if text in DEGREE_TOP_UNIVERSITIES:
        return text
    for degree in DEGREE_TOP_UNIVERSITIES:
        if degree.lower() == text_lower:
            return degree

    # Substring containment — catches "Computer Science" matching an O*NET
    # title like "Computer Systems Analysts" loosely, and vice versa.
    best_match, best_len = None, 0
    for degree in DEGREE_TOP_UNIVERSITIES:
        degree_lower = degree.lower()
        if degree_lower in text_lower or text_lower in degree_lower:
            if len(degree_lower) > best_len:  # prefer the more specific/longer match
                best_match, best_len = degree, len(degree_lower)
    return best_match


# Maps pakistan_resources.py's broad career-field buckets to this file's
# university categories — the two files use different naming, since one
# groups by career field and the other by academic category.
FIELD_TO_UNIVERSITY_CATEGORY = {
    "Software / Technology": "Engineering",
    "Business / Finance": "Business",
    "Engineering": "Engineering",
    "Healthcare / Biology": "Medical",
    "Arts / Design / Media": "Arts / Design",
}


def get_top_universities_for_occupation(occupation_title, career_field=None, limit=3):
    """
    Finds the best real universities for a given O*NET occupation title —
    this is the core "which university is best for this field" feature.

    Strategy, in order:
    1. Match the occupation title against DEGREE_TOP_UNIVERSITIES (the
       authoritative, hand-researched top-7-per-degree ranking) — this is
       real ranking data, not a derived proxy, so it's tried first.
    2. Direct program-name match against a university's notable_programs
       list (substring match, case-insensitive, checked both directions
       since O*NET titles and our program names don't always align
       exactly — e.g. "Software Developers" vs "Software Engineering").
    3. Fall back to the broader academic category (mapped from
       career_field) and return the top-ranked institutions in that
       category.
    Always returns real, curated data — never an invented ranking.
    """
    if not occupation_title:
        return []

    # Attempt 1: authoritative degree ranking
    matched_degree = find_matching_degree(occupation_title)
    if matched_degree:
        return get_top_universities_for_degree(matched_degree, limit=limit)

    title_lower = occupation_title.lower()
    competitiveness_order = {"Highly Competitive": 0, "Competitive": 1, "Moderate": 2}

    # Attempt 2: direct program-name match
    direct_matches = [
        u for u in UNIVERSITIES
        if any(title_lower in p.lower() or p.lower() in title_lower for p in u["notable_programs"])
    ]
    if direct_matches:
        ranked = sorted(direct_matches, key=lambda u: competitiveness_order.get(u["admission_competitiveness"], 3))
        return ranked[:limit]

    # Attempt 3: fall back to the broader academic category
    category = FIELD_TO_UNIVERSITY_CATEGORY.get(career_field)
    if category:
        in_category = get_universities(category)
        ranked = sorted(in_category, key=lambda u: competitiveness_order.get(u["admission_competitiveness"], 3))
        return ranked[:limit]

    return []
