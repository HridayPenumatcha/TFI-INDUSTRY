"""
TFI Nepotism Analysis - Dataset Generator
Generates Excel file with Telugu Film Industry actor data
"""

import pandas as pd
import numpy as np
import os

def create_tfi_dataset():
    # Columns:
    # Name, Gender, Background, Family_Connection, Debut_Year, Age,
    # Total_Movies, Hit_Movies, Blockbuster_Movies, Flop_Movies,
    # Awards_Won, OTT_Projects, Debut_Budget_Cr, Avg_Budget_Cr,
    # Total_BO_Collection_Cr, Highest_BO_Movie, Highest_BO_Cr,
    # Social_Media_Followers_M, Brand_Endorsements,
    # Opportunities_First_3Yrs, Recovery_Chances_After_Flops,
    # Genre_Versatility_Score (1-10), Critical_Acclaim_Score (1-10)

    actors = [
        # ─────────────────── NEPO BACKGROUND ───────────────────
        ("Ram Charan",              "Male",   "Nepo",       "Son of Chiranjeevi",
         2007, 39, 16,  8, 5,  3, 12, 2,  45, 120, 2800, "RRR",                  1200, 25.0, 18,  8,  6,  8,  9),

        ("Jr NTR",                  "Male",   "Nepo",       "Grandson of NT Rama Rao",
         2001, 41, 30, 16, 8,  6, 15, 3,  35, 100, 3200, "RRR",                  1200, 28.0, 20, 12,  5,  9,  8),

        ("Allu Arjun",              "Male",   "Nepo",       "Son of Producer Allu Aravind / Nephew of Chiranjeevi",
         2003, 42, 22, 14, 7,  1, 18, 1,  30, 110, 4500, "Pushpa 2",             1700, 38.0, 25, 10,  5, 10,  8),

        ("Naga Chaitanya",          "Male",   "Nepo",       "Son of Nagarjuna",
         2009, 42, 22,  7, 2, 11,  4, 5,  25,  65,  800, "Love Story",            180, 12.0,  8,  8,  4,  6,  6),

        ("Akhil Akkineni",          "Male",   "Nepo",       "Son of Nagarjuna",
         2015, 30,  8,  1, 0,  6,  1, 1,  40,  70,  350, "Most Eligible Bachelor", 130, 10.0,  6,  5,  5,  2,  5),

        ("Varun Tej",               "Male",   "Nepo",       "Son of Nagendra Babu / Nephew of Chiranjeevi",
         2014, 33, 14,  5, 2,  7,  5, 2,  30,  55,  680, "Ghani",                 120,  8.0,  6,  6,  5,  7,  6),

        ("Sai Dharam Tej",          "Male",   "Nepo",       "Son of Nagendra Babu / Nephew of Chiranjeevi",
         2013, 36, 14,  5, 1,  8,  3, 2,  20,  45,  540, "Solo Brathuke So Better",130,  5.0,  5,  6,  4,  6,  5),

        ("Bellamkonda Sai Sreenivas","Male",  "Nepo",       "Son of Producer Bellamkonda Suresh",
         2014, 31, 11,  3, 1,  7,  2, 0,  35,  60,  420, "Saakshyam",             100,  4.5,  5,  5,  4,  5,  5),

        ("Manchu Manoj",            "Male",   "Nepo",       "Son of Mohan Babu",
         2004, 38, 20,  5, 1, 14,  2, 1,  20,  30,  280, "Julayi",                 55,  3.0,  3,  8,  3,  5,  4),

        ("Manchu Vishnu",           "Male",   "Nepo",       "Son of Mohan Babu",
         2006, 41, 18,  5, 1, 12,  3, 2,  15,  25,  240, "Doosukeltha",            45,  4.0,  4,  7,  3,  5,  5),

        ("Taraka Ratna",            "Male",   "Nepo",       "Nephew of Chiranjeevi",
         2005, 42, 12,  3, 0,  9,  1, 0,  18,  20,  180, "Arjun",                  30,  1.5,  2,  5,  2,  4,  4),

        ("Aadi Saikumar",           "Male",   "Nepo",       "Son of Actor Saikumar",
         2011, 35, 16,  4, 1, 11,  2, 1,  15,  22,  220, "Burrakatha",             40,  2.0,  3,  5,  3,  4,  5),

        ("Nithiin",                 "Male",   "Nepo",       "Son of Producer Sudhakar Reddy",
         2003, 39, 22, 10, 3,  9,  7, 2,  12,  40,  680, "Ishq",                  120,  6.0,  6,  7,  3,  6,  7),

        ("Keerthy Suresh",          "Female", "Nepo",       "Daughter of Director Suresh Kumar & Actress Menaka",
         2013, 32, 28, 12, 4,  8,  8, 6,  15,  35, 1100, "Mahanati",              280, 15.0, 12,  6,  8,  8,  9),

        ("Manchu Lakshmi",          "Female", "Nepo",       "Daughter of Mohan Babu",
         2006, 42, 10,  2, 0,  8,  2, 3,   8,  12,   95, "Aadavallu Meeku Johaarlu", 30,  3.5,  3,  5,  3,  4,  5),

        # ─────────────────── SELF-MADE ───────────────────
        ("Nani",                    "Male",   "Self-Made",  "No industry background",
         2008, 40, 30, 18, 8,  4, 20, 6,   8,  55, 2200, "Dasara",                350, 18.0, 12,  4,  4,  9,  9),

        ("Vijay Deverakonda",       "Male",   "Self-Made",  "No industry background",
         2011, 35, 18,  8, 3,  5, 10, 4,   5,  75, 1600, "Arjun Reddy",           700, 22.0, 10,  3,  3,  8,  8),

        ("Ravi Teja",               "Male",   "Self-Made",  "No industry background",
         1995, 56, 70, 35,12, 23, 15, 4,   3,  35, 1800, "Krack",                 210, 10.0, 12,  4,  4,  7,  7),

        ("Gopichand",               "Male",   "Self-Made",  "No industry background",
         2001, 46, 30, 12, 4, 14,  8, 2,   4,  30,  620, "Loukyam",                95,  4.0,  5,  3,  3,  6,  6),

        ("Adivi Sesh",              "Male",   "Self-Made",  "No industry background",
         2012, 38, 12,  7, 3,  2,  9, 4,   4,  30,  720, "Major",                 260,  8.0,  5,  1,  3,  8,  9),

        ("Naveen Polishetty",       "Male",   "Self-Made",  "No industry background",
         2018, 33,  6,  3, 2,  1,  6, 2,   5,  40,  680, "Agent Sai Srinivasa Athreya", 240, 10.0,  3,  0,  1,  7,  9),

        ("Satya Dev",               "Male",   "Self-Made",  "No industry background",
         2014, 41, 12,  6, 2,  4,  5, 5,   3,  20,  320, "Ranga Ranga Vaibhavanga", 80,  4.0,  3,  1,  2,  7,  8),

        ("Nikhil Siddhartha",       "Male",   "Self-Made",  "No industry background",
         2005, 39, 20,  8, 2, 10,  6, 4,   4,  25,  480, "Karthikeya 2",          240,  5.0,  4,  2,  3,  7,  7),

        ("Karthikeya Gummakonda",   "Male",   "Self-Made",  "No industry background",
         2012, 33, 10,  6, 2,  2,  5, 2,   3,  25,  520, "Karthikeya 2",          240,  6.0,  3,  1,  2,  7,  8),

        ("Priyadarshi Pulikonda",   "Male",   "Self-Made",  "No industry background",
         2016, 36, 18, 10, 3,  5,  6, 8,   2,  15,  350, "Jathi Ratnalu",         120,  5.0,  5,  1,  2,  8,  9),

        ("Sundeep Kishan",          "Male",   "Self-Made",  "No industry background",
         2009, 37, 22,  7, 1, 14,  4, 4,   6,  30,  380, "Michael",                60,  4.0,  4,  2,  3,  6,  6),

        ("Sharwanand",              "Male",   "Self-Made",  "No industry background",
         2007, 38, 22,  9, 2, 11,  7, 4,   8,  40,  560, "Malli Raava",            80,  5.0,  4,  2,  3,  7,  8),

        ("Sudheer Babu",            "Male",   "Self-Made",  "No direct lineage; married into film family later",
         2012, 43, 14,  5, 1,  8,  4, 3,  10,  30,  380, "Nannu Dochukunduvate",   60,  3.0,  4,  1,  3,  6,  6),

        ("Rahul Ramakrishna",       "Male",   "Self-Made",  "No industry background",
         2015, 37, 20,  9, 3,  5,  4, 6,   1,   8,  280, "Arjun Reddy",           700,  3.0,  3,  0,  2,  9,  9),

        ("Sunil",                   "Male",   "Self-Made",  "No industry background",
         2001, 51, 40, 15, 4, 21,  8, 3,   2,  15,  380, "Julayi",                 40,  2.5,  3,  2,  3,  6,  7),

        ("Anand Deverakonda",       "Male",   "Self-Made",  "Brother of Vijay Deverakonda (borderline - post-brother fame)",
         2019, 30,  5,  2, 0,  3,  1, 2,   5,  25,  120, "Middle Class Melodies",   40,  4.0,  4,  1,  1,  5,  6),

        # ─────────────────── ACTRESSES – SELF-MADE ───────────────
        ("Rashmika Mandanna",       "Female", "Self-Made",  "No industry background",
         2016, 29, 22, 14, 7,  1, 12, 4,   8,  45, 1800, "Pushpa",                950, 30.0, 18,  1,  1,  9,  8),

        ("Samantha Ruth Prabhu",    "Female", "Self-Made",  "No industry background",
         2010, 38, 28, 16, 5,  5, 15, 8,  10,  50, 1600, "Yashoda",               350, 25.0, 14,  3,  3,  9,  9),

        ("Kajal Aggarwal",          "Female", "Self-Made",  "No industry background",
         2008, 39, 35, 18, 6,  9, 10, 4,   8,  40, 1400, "Magadheera",            650, 20.0, 12,  2,  3,  8,  7),

        ("Tamannaah Bhatia",        "Female", "Self-Made",  "No industry background",
         2005, 35, 70, 25, 8, 25,  8, 6,   8,  40, 1600, "Baahubali",             800, 22.0, 14,  3,  4,  7,  7),

        ("Sreeleela",               "Female", "Self-Made",  "No industry background",
         2021, 24, 10,  5, 2,  3,  5, 2,  10,  40,  650, "Guntur Kaaram",         180, 18.0,  6,  0,  1,  8,  8),

        ("Anupama Parameswaran",    "Female", "Self-Made",  "No industry background",
         2015, 29, 22, 10, 2,  8,  6, 4,   5,  20,  480, "A..Aa",                 140,  8.0,  8,  1,  2,  7,  8),

        ("Krithi Shetty",           "Female", "Self-Made",  "No industry background",
         2021, 24, 10,  6, 2,  2,  4, 3,  10,  30,  420, "Uppena",                180,  8.0,  5,  0,  1,  7,  8),

        ("Nithya Menen",            "Female", "Self-Made",  "No industry background",
         2007, 38, 55, 28, 8, 15, 18, 8,   5,  25, 1200, "OK Bangaram",           280,  8.0, 10,  2,  4,  9, 10),

        ("Pooja Hegde",             "Female", "Self-Made",  "No industry background",
         2012, 34, 30, 15, 5,  8,  8, 4,  10,  45, 1400, "Ala Vaikunthapuramulo", 850, 20.0, 12,  2,  3,  8,  7),

        ("Ritu Varma",              "Female", "Self-Made",  "No industry background",
         2015, 33, 15,  8, 2,  5,  5, 6,   5,  20,  380, "Pellichoopulu",         120,  5.0,  5,  1,  2,  7,  9),

        ("Regina Cassandra",        "Female", "Self-Made",  "No industry background",
         2010, 35, 30, 12, 2, 14,  6, 6,   4,  18,  450, "Evade Subramanyam",      80,  6.0,  5,  2,  3,  7,  8),

        ("Hebah Patel",             "Female", "Self-Made",  "No industry background",
         2015, 31, 18,  8, 2,  7,  4, 5,   4,  15,  300, "Mister",                 80,  4.0,  6,  1,  2,  7,  8),

        ("Payal Rajput",            "Female", "Self-Made",  "No industry background",
         2018, 32, 10,  5, 2,  3,  3, 3,   5,  20,  280, "RX 100",                 80,  5.0,  5,  0,  1,  7,  7),

        ("Eesha Rebba",             "Female", "Self-Made",  "No industry background",
         2016, 30, 12,  5, 1,  6,  3, 3,   4,  15,  220, "Aravindha Sametha",      50,  3.5,  4,  1,  2,  6,  7),
    ]

    columns = [
        "Name", "Gender", "Background", "Family_Connection", "Debut_Year", "Age",
        "Total_Movies", "Hit_Movies", "Blockbuster_Movies", "Flop_Movies",
        "Awards_Won", "OTT_Projects",
        "Debut_Budget_Cr", "Avg_Budget_Cr", "Total_BO_Collection_Cr",
        "Highest_BO_Movie", "Highest_BO_Amount_Cr",
        "Social_Media_Followers_M", "Brand_Endorsements",
        "Opportunities_First_3Yrs", "Recovery_Chances_After_Flops",
        "Genre_Versatility_Score", "Critical_Acclaim_Score"
    ]

    df = pd.DataFrame(actors, columns=columns)
    df.insert(0, "Actor_ID", range(1, len(df) + 1))

    # ── Derived Metrics ──────────────────────────────────────────────
    df["Years_in_Industry"]      = 2025 - df["Debut_Year"]
    df["Avg_Movies_Per_Year"]    = (df["Total_Movies"] / df["Years_in_Industry"]).round(2)
    df["Success_Rate_Pct"]       = ((df["Hit_Movies"] + df["Blockbuster_Movies"]) / df["Total_Movies"] * 100).round(1)
    df["Flop_Rate_Pct"]          = (df["Flop_Movies"] / df["Total_Movies"] * 100).round(1)
    df["BO_Per_Movie_Cr"]        = (df["Total_BO_Collection_Cr"] / df["Total_Movies"]).round(1)
    df["Budget_ROI_Ratio"]       = (df["Total_BO_Collection_Cr"] / (df["Avg_Budget_Cr"] * df["Total_Movies"])).round(2)
    df["Background_Binary"]      = (df["Background"] == "Nepo").astype(int)   # 1=Nepo, 0=Self-Made
    df["Debut_Budget_Advantage"] = df.apply(
        lambda r: "High" if r["Debut_Budget_Cr"] >= 30 else ("Mid" if r["Debut_Budget_Cr"] >= 15 else "Low"), axis=1
    )

    # Career tier
    def career_tier(row):
        if row["Success_Rate_Pct"] >= 65 and row["Total_BO_Collection_Cr"] >= 1000:
            return "Superstar"
        elif row["Success_Rate_Pct"] >= 50 and row["Total_BO_Collection_Cr"] >= 400:
            return "A-List"
        elif row["Success_Rate_Pct"] >= 35:
            return "Mid-Tier"
        else:
            return "Struggling"

    df["Career_Tier"] = df.apply(career_tier, axis=1)

    # Opportunity Index  (normalised 0-10 for cluster comparability)
    df["Opportunity_Index"] = (
        df["Opportunities_First_3Yrs"] * 0.5 +
        df["Recovery_Chances_After_Flops"] * 0.5 +
        df["Debut_Budget_Cr"] / 10
    ).round(2)

    return df


if __name__ == "__main__":
    df = create_tfi_dataset()
    out_path = "TFI_Nepotism_Analysis.xlsx"
    df.to_excel(out_path, index=False)
    print(f"✅  Dataset saved → {out_path}  ({len(df)} actors, {len(df.columns)} columns)")
    print(df[["Name", "Background", "Success_Rate_Pct", "Career_Tier"]].to_string(index=False))
