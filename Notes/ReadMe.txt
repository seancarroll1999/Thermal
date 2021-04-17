STRUCTURE
    *   Logic:
            ->  Api_Calls
                    -   Every Api call code has its file here (base classes of common API implementations (RapidAPI stored here))
    *   Storage:
            ->  API_Headers
                    -   CSV Files containing the most recent header calls (Important for calls with limited uses)
            ->  API_History
                    -   CSV Files containing hashes of API bodies, will prevent against the same content being presented to the user
            -   QuizHistory.CSV:
                    -   Any quiz element of Thermal will be stored here in a [Question:Answer] format, this will allow printing of answers from app



(Momentary LED swtich PI tutorial: https://www.instructables.com/Add-Adafruits-Ring-LED-Momentary-Switch-to-Raspber/)