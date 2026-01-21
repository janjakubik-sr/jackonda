**************************************
jackonda
by Jan Jakubik (jakubik@biomed.cas.cz)
Creative Commons Licence BY-NC
**************************************
Jackonda is a set of Python scripts for the analysis of pharmacodynamic data by non-linear regression fitting of various equations to the experimental data.

How it works:
Jackonda assumes that each experiment has its own folder and (preprocessed) data for each curve to be fitted are in separate *.dat files. Data should be arranged column-wise in x, y, dy order, separated either by spaces or tabs, without legends and row index. Please look at the "Examples" folder. Data may be manually edited or rearranged using scripts in the "Data" menu.

1) Jackonda works only with data in the working directory, so before you start, select your working directory from the File menu.
2) Edit your data if necessary from the Edit menu.
3) Batch analyse data by selecting the type of experiment from the Batch Analysis menu.
4) Scripts are fully automatic with checks for errors, data formatting, whether the number of data points is sufficient for analysis, etc.
5) Scripts will take all *.dat files in your current folder one by one, analyse them, log to the main window, save the results to *.res file, create *.draw file for making fancy graphs with Grace and make a simple preview graph of the analysis.
6) In interactive mode you choose file(s) you want to analyse
6) Finalise your graph in Grace by selecting "Plot results with Grace" from the "Results" menu and SAVE it.
7) You may analyse data using different equations. Jaconda will create separate files with results (*.res) and drawing instructions (*.draw) for each analysis. Repeating the same analysis will overwrite previous results.
8) Jackonda may fail in fitting, or you may not like the results. You can then try interactive fitting by guiding Jackonda with your own estimates and limits. However, be advised that in such a case, it is very likely that the data or the choice of equation is bad.

Selected types of experiments:
Allosteric interaction
y = 100*(D + KD) / (D + (KD*(KA+10^x))/(KA+(10^x)/alpha))
where y is binding at concentration of allosteric modulator x, D is the concentration of radioligand, and KD is its equilibrium dissociation constant. The X-axis is logarithmic. Equilibrium dissociation constant of allosteric modulator KA and factor of cooperativity alpha are calculated.
Ref. Ehlert FJ (1988) Estimation of the affinities of allosteric ligands using radioligand binding and pharmacological null methods. Mol Pharmacol 33: 187-194.

Association
y = Beq * (1 - exp(-kon * x))
where y is binding at time. The X-axis is linear. Binding at equilibrium (Beq) and apparent association rate (kon) are calculated.

Competition
y = 100 - 100 * 10^(x*nH) / (IC50^nH + 10^(x*nH))
where y is binding at concentration x. The X-axis is logarithmic. Concentration causing 50 % inhibition (IC50) and Hill coefficient (nH) are calculated.

Dissociation
y = 100 * exp(-koff * x)
where y is the binding at time x expressed as a percentage of the binding at the beginning of dissociation. The X-axis is linear. Dissociation rate koff is calculated.

Functional response
y = basal + (Emax - basal) / (1 + 10^((EC50 -x)*nH))
where Y is the response at concentration x. The X-axis is logarithmic. Basal response, concentration causing 50% of response (EC50), maximal response (Emax) and Hill coefficient (nH) are calculated.

Saturation
y = Bmax * x / (KD + x)
where y is binding at concentration x. The X-axis is linear. Maximum binding capacity Bmax and equilibrium dissociation constant KD are calculated.

3-ligands (two orthosteric and one allosteric)
y = 100*(D + KD) / (D + KD*(I*(KA + (10^x)/beta) + Ki*(KA+10^x))/(Ki*(KA + (10^x)/alpha)))


alphaKD from dissociation rates
y = koff * (alphaKD^nH) / (alphaKD^nH + 10^(x*nH))
where y is the dissociation rate at concentration of allosteric modulator x, and koff is the dissociation rate in the absence of allosteric modulator. The X-axis is logarithmic. Equilibrium dissociation constant of allosteric modulator to receptor-radioligand complex, alphaKD and Hill coefficient (nH) are calculated.
Ref. Lazareno S and Birdsall NJ (1995) Detection, quantitation, and verification of allosteric interactions of agents with labelled and unlabeled ligands at G protein-coupled receptors: interactions of strychnine and acetylcholine at muscarinic receptors. Mol Pharmacol 48: 362-378.

Functional response
Various equations for functional responses

OMA
Various equations for operatinal model of agonism. Refs. Jakubík et Randáková (2022). Insights into the operational model of agonism of receptor dimers. Expert Opin Drug Discov 17: 1181–1191.  Jakubík et al. (2020). The operational model of allosteric modulation of pharmacological agonism. Sci Rep 10: 14421. Jakubík et al. (2019). Applications and limitations of fitting of the operational model to determine relative efficacies of agonists. Sci Rep 9: 4637. Randáková et al. (2023). A critical re-evaluation of the slope factor of the operational model of agonism: When to exponentiate operational efficacy. Sci Rep 13: 17587.

Schild analysis
for competitive interaction
y = [B] - logKB
for allosteric interaction
y = log([B]*(1-alpha)/(aplha*[B]+KB))
where y is log(DR -), e.g. log (EC50'/EC50 -1), and KB is the equilibrium dissociation constant of an antagonist. The X-axis is logarithmic.

Models
The Models menu offers theoretical modelling (no fitting) of complex models.
