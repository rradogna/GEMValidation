import sys

from ROOT import *

from cuts import *
from drawPlots import *

## run quiet mode
import sys
sys.argv.append( '-b' )

import ROOT 
ROOT.gROOT.SetBatch(1)

if __name__ == "__main__":  

  inputFile = '/cmshome/radogna/GEM_Geometry/cesare_rel/CMSSW_6_2_0_SLHC5/src/gem_localrec_ana.root'
  outputFile = 'gem_localrec_ana_tmp.root'
  targetDir = './'
  
  ## extension for figures - add more?
  ext = ".png"
  
  ## GEM system settings
  nregion = 2
  nlayer = 2
  npart = 8
  bx_times_25ns = 9*0.000000025
  nchambers_ge11=144
  nchambers_ge21=77
  
  ## Trees
  analyzer = "GEMRecHitAnalyzer"
  recHitsNoise = "GEMRecHitNoiseTree"
  events = "GEMEventsTree"
  
  ## Style
  gStyle.SetStatStyle(0);

  ## input
  file = TFile.Open(inputFile)
  if not file:
    sys.exit('Input ROOT file %s is missing.' %(inputFile))

  dirAna = file.Get(analyzer)
  if not dirAna:
    sys.exit('Directory %s does not exist.' %(dirAna))
        
  treeEvents = dirAna.Get(events)
  if not treeEvents:
    sys.exit('Tree %s does not exist.' %(treeEvents))


  Nentries = treeEvents.GetEntriesFast()
  print Nentries
  file.Close()
  
  file = TFile.Open(inputFile)
  if not file:
    sys.exit('Input ROOT file %s is missing.' %(inputFile))

  dirAna = file.Get(analyzer)
  if not dirAna:
    sys.exit('Directory %s does not exist.' %(dirAna))
  
  treeHits = dirAna.Get(recHitsNoise)
  if not treeHits:
    sys.exit('Tree %s does not exist.' %(treeHits))
  print Nentries

  fileOut = TFile.Open(outputFile, "RECREATE")  
#-------------------------------------------------------------------------------------------------------------------------------------#
  #gStyle.SetStatStyle(0)
  #gStyle.SetOptStat(1110)
  c = TCanvas("c","c",800,800)
  c.Clear()

     
  h1 = TH1F("h1", "GEM RecHit noise rate per roll number,station1;roll number;rate [Hz/cm^{-2}]",13,0.,13.)
  h2 = TH1F("h2", "GEM RecHit noise rate per roll number,station2;roll number;rate [Hz/cm^{-2}]",13,0.,13.)
  h3 = TH1F("h3", "GEM RecHit noise rate per roll number,station3;roll number;rate [Hz/cm^{-2}]",13,0.,13.)
  
  print "Making plots for noise rate: ",
  entries = treeHits.GetEntriesFast()
  for jentry in xrange(entries):
      ientry = treeHits.LoadTree( jentry )
      if ientry < 0:
        break
    
      treeHits.GetEntry(jentry) 
      #print treeHits.roll
      area_roll = treeHits.trArea
      scale = 1/(area_roll*bx_times_25ns*nchambers_ge11*Nentries)
      #print area_roll
      #print "area ", area_roll,  "scale", scale
      if treeHits.station==1:
        #h1.Fill(treeHits.roll, treeHits.trArea*bx_times_25ns*nchambers_ge11/Nentries) 
	h1.Fill(treeHits.roll, 1/(area_roll*bx_times_25ns*nchambers_ge11*Nentries)) 
      if treeHits.station==2:
        h2.Fill(treeHits.roll, 1/(area_roll*bx_times_25ns*nchambers_ge21*Nentries))
      if treeHits.station==3:
        h3.Fill(treeHits.roll, 1/(area_roll*bx_times_25ns*nchambers_ge21*Nentries))
      if (jentry+1) % 30000 == 0: 
            sys.stdout.write("."); sys.stdout.flush()
  print " done."
    #his.SetBinContent(1, h.GetBinContent(1)*2)

  h1.SetTitle("GEM RecHit noise rate per roll number,station1;roll number;rate [Hz/cm^{-2}]")
  h1.SetStats(0)
  h1.SetLineWidth(2)
  h1.SetLineColor(kBlue)
  h1.Draw("HIST TEXT")
  #his.SetMinimum(0.)
  c.SaveAs(targetDir + "noise_rate_s1" + ext)
  h2.SetTitle("GEM RecHit noise rate per roll number,station2;roll number;rate [Hz/cm^{-2}]")
  h2.SetStats(0)
  h2.SetLineWidth(2)
  h2.SetLineColor(kBlue)
  h2.Draw("HIST TEXT")
  c.SaveAs(targetDir + "noise_rate_s2" + ext)
  h3.SetTitle("GEM RecHit noise rate per roll number,station3;roll number;rate [Hz/cm^{-2}]")
  h3.SetStats(0)
  h3.SetLineWidth(2)
  h3.SetLineColor(kBlue)
  h3.Draw("HIST TEXT")
  c.SaveAs(targetDir + "noise_rate_s3" + ext)  
  
  draw_1D(targetDir, "occupancy_per_roll_s1", ext, treeHits, "GEM RecHit occupancy per roll number,station1;roll number;entries", 
  	 "h_", "(14,-0.5,13.5)", "roll", TCut("station==1"), "HIST TEXT")
  draw_1D(targetDir, "occupancy_per_roll_s2", ext, treeHits, "GEM RecHit occupancy per roll number,station2;roll number;entries",
         "h_", "(14,-0.5,13.5)", "roll", TCut("station==2"), "HIST TEXT")
  draw_1D(targetDir, "occupancy_per_roll_s3", ext, treeHits, "GEM RecHit occupancy per roll number,station3;roll number;entries",
         "h_", "(14,-0.5,13.5)", "roll", TCut("station==3"), "HIST TEXT")
	 
	 
#-------------------------------------------------------------------------------------------------------------------------------------#

  draw_1D(targetDir, "clsDistribution", ext, treeHits, "CLS; CLS; entries", "h_", "(11,-0.5,10.5)", "clusterSize", TCut(""), "");

  draw_1D(targetDir, "clsDistribution_rm1_l1", ext, treeHits, "CLS region-1, layer1; CLS; entries", 
	   "h_", "(11,-0.5,10.5)", "clusterSize", AND(rm1,l1), "");
  draw_1D(targetDir, "clsDistribution_rm1_l2", ext, treeHits, "CLS region-1, layer2; CLS; entries", 
	   "h_", "(11,-0.5,10.5)", "clusterSize", AND(rp1,l2), "");
  draw_1D(targetDir, "clsDistribution_rp1_l1", ext, treeHits, "CLS region1, layer1; CLS; entries", 
	   "h_", "(11,-0.5,10.5)", "clusterSize", AND(rm1,l1), "");
  draw_1D(targetDir, "clsDistribution_rp1_l2", ext, treeHits, "CLS region1, layer2; CLS; entries", 
	   "h_", "(11,-0.5,10.5)", "clusterSize", AND(rp1,l2), "");

#-------------------------------------------------------------------------------------------------------------------------------------#

  draw_1D(targetDir, "bxDistribution", ext, treeHits, "BX; BX; entries", 
	   "h_", "(13,-6.5,6.5)", "bx", TCut(""), "");

  draw_1D(targetDir, "bxDistribution_st1", ext, treeHits, "BX (station 1); BX; entries", 
	   "h_", "(13,-6.5,6.5)", "bx", TCut("station==1"), "");
  draw_1D(targetDir, "bxDistribution_st2", ext, treeHits, "BX (station 2); BX; entries", 
	   "h_", "(13,-6.5,6.5)", "bx", TCut("station==2"), "");
  draw_1D(targetDir, "bxDistribution_st3", ext, treeHits, "BX (station 3); BX; entries", 
	   "h_", "(13,-6.5,6.5)", "bx", TCut("station==3"), "");

#-------------------------------------------------------------------------------------------------------------------------------------#

 
  draw_1D(targetDir, "strip_rh_rm1_l1", ext, treeHits, "GEM RecHit occupancy per strip number, region-1 layer1;strip number;entries", 
	  "h_", "(384,0.5,384.5)", "firstClusterStrip", AND(rm1,l1))
  draw_1D(targetDir, "strip_rh_rm1_l2", ext, treeHits, "GEM RecHit occupancy per strip number, region-1 layer2;strip number;entries", 
	  "h_", "(384,0.5,384.5)", "firstClusterStrip", AND(rm1,l2))
  draw_1D(targetDir, "strip_rh_rp1_l1", ext, treeHits, "GEM RecHit occupancy per strip number, region1 layer1;strip number;entries", 
	  "h_", "(384,0.5,384.5)", "firstClusterStrip", AND(rp1,l1))
  draw_1D(targetDir, "strip_rh_rp1_l2", ext, treeHits, "GEM RecHit occupancy per strip number, region1 layer2;strip number;entries", 
	  "h_", "(384,0.5,384.5)", "firstClusterStrip", AND(rp1,l2))
#-------------------------------------------------------------------------------------------------------------------------------------#
  draw_2D_adv(targetDir, "roll_vs_strip_rh", ext, treeHits, "GEM RecHit occupancy per roll and strip number;strip number;roll", 
	  "h_", "(768,0.5,768.5,12,0.5,12.5)", "firstClusterStrip:roll", TCut(""), "COLZ")

  draw_2D_adv(targetDir, "roll_vs_strip_rh_rm1_st1_l1", ext, treeHits, "GEM RecHit occupancy per roll and strip number, region-1 layer1 station1;strip number;roll", "h_", "(384,0.5,384.5,12,0.5,12.5)", "firstClusterStrip:roll", AND(rm1,l1,st1), "COLZ")
  draw_2D_adv(targetDir, "roll_vs_strip_rh_rm1_st1_l2", ext, treeHits, "GEM RecHit occupancy per roll and strip number, region-1 layer2 station1;strip number;roll", "h_", "(384,0.5,384.5,12,0.5,12.5)", "firstClusterStrip:roll", AND(rm1,l2,st1), "COLZ")
  draw_2D_adv(targetDir, "roll_vs_strip_rh_rp1_st1_l1", ext, treeHits, "GEM RecHit occupancy per roll and strip number, region1 layer1 station1;strip number;roll", "h_", "(384,0.5,384.5,12,0.5,12.5)", "firstClusterStrip:roll", AND(rp1,l1,st1), "COLZ")
  draw_2D_adv(targetDir, "roll_vs_strip_rh_rp1_st1_l2", ext, treeHits, "GEM RecHit occupancy per roll and strip number, region1 layer2 station1;strip number;roll", "h_", "(384,0.5,384.5,12,0.5,12.5)", "firstClusterStrip:roll", AND(rp1,l2,st1), "COLZ")

  draw_2D_adv(targetDir, "roll_vs_strip_rh_rm1_st2_l1", ext, treeHits, "GEM RecHit occupancy per roll and strip number, region-1 layer1 station2;strip number;roll", "h_", "(768,0.5,768.5,12,0.5,12.5)", "firstClusterStrip:roll", AND(rm1,l1,st2), "COLZ")
  draw_2D_adv(targetDir, "roll_vs_strip_rh_rm1_st2_l2", ext, treeHits, "GEM RecHit occupancy per roll and strip number, region-1 layer2 station2;strip number;roll", "h_", "(768,0.5,768.5,12,0.5,12.5)", "firstClusterStrip:roll", AND(rm1,l2,st2), "COLZ")
  draw_2D_adv(targetDir, "roll_vs_strip_rh_rp1_st2_l1", ext, treeHits, "GEM RecHit occupancy per roll and strip number, region1 layer1 station2;strip number;roll", "h_", "(768,0.5,768.5,12,0.5,12.5)", "firstClusterStrip:roll", AND(rp1,l1,st2), "COLZ")
  draw_2D_adv(targetDir, "roll_vs_strip_rh_rp1_st2_l2", ext, treeHits, "GEM RecHit occupancy per roll and strip number, region1 layer2 station2;strip number;roll", "h_", "(768,0.5,768.5,12,0.5,12.5)", "firstClusterStrip:roll", AND(rp1,l2,st2), "COLZ")

  draw_2D_adv(targetDir, "roll_vs_strip_rh_rm1_st3_l1", ext, treeHits, "GEM RecHit occupancy per roll and strip number, region-1 layer1 station3;strip number;roll", "h_", "(768,0.5,768.5,12,0.5,12.5)", "firstClusterStrip:roll", AND(rm1,l1,st3), "COLZ")
  draw_2D_adv(targetDir, "roll_vs_strip_rh_rm1_st3_l2", ext, treeHits, "GEM RecHit occupancy per roll and strip number, region-1 layer2 station3;strip number;roll", "h_", "(768,0.5,768.5,12,0.5,12.5)", "firstClusterStrip:roll", AND(rm1,l2,st3), "COLZ")
  draw_2D_adv(targetDir, "roll_vs_strip_rh_rp1_st3_l1", ext, treeHits, "GEM RecHit occupancy per roll and strip number, region1 layer1 station3;strip number;roll", "h_", "(768,0.5,768.5,12,0.5,12.5)", "firstClusterStrip:roll", AND(rp1,l1,st3), "COLZ")
  draw_2D_adv(targetDir, "roll_vs_strip_rh_rp1_st3_l2", ext, treeHits, "GEM RecHit occupancy per roll and strip number, region1 layer2 station3;strip number;roll", "h_", "(768,0.5,768.5,12,0.5,12.5)", "firstClusterStrip:roll", AND(rp1,l2,st3), "COLZ")


#-------------------------------------------------------------------------------------------------------------------------------------#


 
  file.Close()
  fileOut.Close()
  
