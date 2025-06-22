# Массив меток
LABELS = ["γ", "e+", "e-", "μ+", "μ-", "π+", "π-", "p", "p-", "K+", "K-"]

PUMPINGS = [
    "MHAD2010",
    "MHAD2011",
    "MHAD2012",
    "MHAD2017",
    "MHAD2019",
    "MHAD2020",
    "MHAD2021",
    "MHAD2022",
    "MHAD2023",
    "MHAD2024",
    "RHO_2013",
    "RHO_2018",
    "RHO_2019",
    "RHO_2024",
    "PHI_2024",
]

LATEST_PUMPINGS = [
    "MHAD2010-4",
    "MHAD2011-6",
    "MHAD2012-6",
    "MHAD2017-6",
    "MHAD2019-3",
    "MHAD2020-3",
    "MHAD2021-2",
    "MHAD2022-3",
    "MHAD2023-2",
    "MHAD2024-2",
    "RHO_2013-4",
    "RHO_2018-8",
    "RHO_2019-2",
    "RHO_2024-0",
    "PHI_2024-0"]

NTUPLE_VARS = ['run', 'event', 'trin', 'beam', 'nc', 'nn', 'etot', 'eton', 'ptrn', 'plrn', 'ptrt', 'nwo{0:255}/I',
               'nwr{0:255}/I', 'wrn[nwr]/I', 'wrt[nwr]/D', 'wramp[nwr]/D', 'wrz[nwr]/D', 'nst{0:255}/I', 'stz[nst]/D',
               'stdz[nst]/D', 'sts[nst]/I', 'stk[nst]/I', 'str[nst]/I', 'sta[nst]/D', 'sti[nst]/D', 'cosm', 'act{0:1}',
               'cact{0:1}', 'np{0:31}/I', 'charge[np]', 'energy[np]', 'theta[np]', 'phi[np]', 'thetac[np]', 'phic[np]',
               'z0[np]', 'd0[np]', 'thetaS[np]', 'phis[np]', 'cnp{0:31}', 'cenergy[cnp]/F', 'cenergyerr[cnp]/F',
               'cdirx[cnp]', 'cdiry[cnp]', 'cdirz[cnp]', 'cphi[cnp]/F', 'ctheta[cnp]/F', 'cDphi[cnp]/F',
               'cDtheta[cnp]/F', 'cetot', 'cx2g[cnp]/F', 'emcMinTime[cnp]', 'emcMeanTime[cnp]', 'emcThetaMean[np]',
               'emcPhiMean[np]', 'el1[cnp]/F', 'el2[cnp]/F', 'el3[cnp]/F', 'npoi{0:31}/I', 'xPoi[npoi]/D',
               'xSig2[npoi]/D', 'yPoi[npoi]/D', 'ySig2[npoi]/D', 'zPoi[npoi]/D', 'zSig2[npoi]/']
DISCRIMINATORS = ['Cuts', 'CutsD', 'CutsPCA', 'CutsGA', 'Likelihood', 'LikelihoodD', 'LikelihoodPCA', 'LikelihoodKDE', 'LikelihoodMIX', 'PDERS', 'PDERSkNN', 'PDERSD', 'PDERSPCA', 'KNN', 'HMatrix', 'Fisher', 'FDA_GA', 'FDA_MC', 'FDA_SA', 'FDA_MT', 'FDA_GAMT', 'FDA_MCMT', 'MLP', 'CFMlpANN', 'TMlpANN', 'BDT', 'BDTD', 'RuleFit', 'RuleFitJF', 'SVM_Gauss', 'SVM_Poly', 'SVM_Lin', 'Plugin']


EXTENDED_PUMPINGS = [
'MHAD2010-4',
'MHAD2011-6',
'MHAD2012-6',
'MHAD2017-4',
'MHAD2017-5',
'MHAD2017-6',
'MHAD2019-2',
'MHAD2019-3',
'MHAD2020-1',
'MHAD2020-3',
'MHAD2021-1',
'MHAD2021-2',
'MHAD2022-3',
'MHAD2023-0',
'MHAD2023-1',
'MHAD2023-2',
'MHAD2024-0',
'MHAD2024-1',
'MHAD2024-2',
'RHO_2013-4',
'RHO_2018-2',
'RHO_2018-3',
'RHO_2018-4',
'RHO_2018-5',
'RHO_2018-6',
'RHO_2018-8',
'RHO_2019-1',
'RHO_2019-2',
'RHO_2024-0',
'PHI_2024-0']

EXTENDED_PUMPINGS_RELEASE = [
'MHAD2010-4 (R006-004)',
'MHAD2011-6 (R006-004)',
'MHAD2012-6 (R006-004)',
'MHAD2017-4 (R006-004)',
'MHAD2017-5 (R006-004)',
'MHAD2017-6 (R008-002)',
'MHAD2019-2 (R007-001)',
'MHAD2019-3 (R008-002)',
'MHAD2020-1 (R007-001)',
'MHAD2020-3 (R008-002)',
'MHAD2021-1 (R007-001)',
'MHAD2021-2 (R008-002)',
'MHAD2022-3 (R008-002)',
'MHAD2023-0 (R008-002)',
'MHAD2023-1 (R008-002)',
'MHAD2023-2 (R008-003)',
'MHAD2024-0 (R008-002)',
'MHAD2024-1 (R008-002)',
'MHAD2024-2 (R008-003)',
'RHO_2013-4 (R006-004)',
'RHO_2018-2 (R006-004)',
'RHO_2018-3 (R006-004)',
'RHO_2018-4 (R008-001)',
'RHO_2018-5 (R008-001)',
'RHO_2018-6 (R008-002)',
'RHO_2018-8 (R010-002)',
'RHO_2019-1 (R007-001)',
'RHO_2019-2 (R008-002)',
'RHO_2024-0 (R008-003)',
'PHI_2024-0 (R008-003)']



TMVA_GUI_BUTTONS = [
    "(1a) Input Variables",
    "(1b) Decorrelated Input Variables",
    "(1c) PCA-transformed Input Variables",
    "(2a) Input Variable Correlations (scatter profiles)",
    "(2b) Decorrelated Input Variable Correlations (scatter profiles)",
    "(2c) PCA-transformed Input Variable Correlations (scatter profiles)",
    "(3) Input Variable Linear Correlation Coefficients",
    "(4a) Classifier Output Distributions",
    "(4b) Classifier Output Distributions for Training and Test Samples",
    "(4c) Classifier Probability Distributions",
    "(4d) Classifier Rarity Distributions",
    "(5a) Classifier Cut Efficiencies",
    "(5b) Classifier Background Rejection vs Signal Efficiency (ROC curve)",
    "(6) Likelihood Reference Distributions",
    "(7a) Network Architecture",
    "(7b) Network Convergence Test",
    "(8) Decision Trees",
    "(9) PDFs of Classifiers",
    "(10) Rule Ensemble Importance Plots",
    "(11) Quit"
]

TMVA_IMAGES = [
    "variables_0.png",                # Input Variables
    "variables_1.png",                # Decorrelated Input Variables
    "variables_2.png",                # PCA-transformed Input Variables
    "CorrelationProfiles_0.png",      # Input Variable Correlations
    "CorrelationProfiles_1.png",      # Decorrelated Input Variable Correlations
    "CorrelationProfiles_2.png",      # PCA-transformed Input Variable Correlations
    "LinearCorrelations.png",         # Input Variable Linear Correlation Coefficients
    "ClassifierOutputs.png",          # Classifier Output Distributions
    "ClassifierProbabilities.png",    # Classifier Probability Distributions
    "ClassifierRarities.png",         # Classifier Rarity Distributions
    "TrainTestComparison.png",        # Classifier Outputs (Training/Test)
    "ROCCurve.png",                   # Classifier Background Rejection vs Signal Efficiency
    "LikelihoodReference.png",        # Likelihood Reference Distributions
    "MLP_Architecture.png",           # Network Architecture
    "MLP_ConvergenceTest.png",        # Network Convergence Test
    "BDT_DecisionTree.png",           # Decision Trees
    "ClassifierPDFs.png",             # PDFs of Classifiers
    "RuleEnsembleImportance.png"      # Rule Ensemble Importance Plots
]


TMVA_IMAGE_BUTTON = [
    ("(1a) Input Variables", "variables_c1.png"),
    ("(1b) Decorrelated Input Variables", "variables_decorr_c2.png"),
    ("(1c) PCA-transformed Input Variables", "variables_decorr_c2.png"),
    ("(2a) Input Variable Correlations (scatter profiles)", "CorrelationProfiles_0.png"),
    ("(2b) Decorrelated Input Variable Correlations (scatter profiles)", "CorrelationProfiles_1.png"),
    ("(2c) PCA-transformed Input Variable Correlations (scatter profiles)", "CorrelationProfiles_2.png"),
    ("(3) Input Variable Linear Correlation Coefficients", "LinearCorrelations.png"),
    ("(4a) Classifier Output Distributions", "ClassifierOutputs.png"),
    ("(4b) Classifier Output Distributions for Training and Test Samples", "overtrain_Fisher.png"),
    ("(4c) Classifier Probability Distributions", "proba_Fisher.png"),
    ("(4d) Classifier Rarity Distributions", "rariry_Fisher.png"),
    ("(5a) Classifier Background Rejection vs Signal Efficiency (ROC curve)", "rejBvsS.png"),
    ("(6) Likelihood Reference Distributions", "LikelihoodReference.png"),
    ("(7a) Network Architecture", "MLP_Architecture.png"),
    ("(7b) Network Convergence Test", "MLP_ConvergenceTest.png"),
    ("(8) Decision Trees", "BDT_DecisionTree.png"),
    ("(9) PDFs of Classifiers", "ClassifierPDFs.png"),
    ("(10) Rule Ensemble Importance Plots", "RuleEnsembleImportance.png"),
]
