#include <iostream>
#include "TClonesArray.h"
#include "TFile.h"
#include "TChain.h"
#include "TH1F.h"
#include "TH2F.h"
#include "/x5/cms/jwkim/Delphes_NEW/Delphes3.4.2/classes/DelphesClasses.h"

using namespace std;

int main(int argc, char** argv){

	 TFile* outFile = new TFile(argv[1],"recreate");
     TChain* inChain = new TChain("Delphes");

     int    nttype = atoi(argv[2]) ; // singla:1 BKG: 0
     double ntxsec = atof(argv[3]) ;

    for(int iFile = 4; iFile<argc; iFile++) {
        std::cout << "### InFile " << iFile-1 << " " << argv[iFile] << std::endl;
        inChain->Add(argv[iFile]);
    }



	TClonesArray* eleTCA = new TClonesArray("Electron");inChain->SetBranchAddress("Electron",&eleTCA);
    TClonesArray *phoTCA = new TClonesArray("Photon"); inChain->SetBranchAddress("Photon",&phoTCA);
    TClonesArray *jetTCA = new TClonesArray("Jet"); inChain->SetBranchAddress("Jet",&jetTCA);
    TClonesArray *TowerTCA = new TClonesArray("Tower"); inChain->SetBranchAddress("Tower",&TowerTCA);
    TClonesArray *TrackTCA = new TClonesArray("Track"); inChain->SetBranchAddress("Track",&TrackTCA);

    TClonesArray *eleSelTCA =  new TClonesArray("Electron");
    TClonesArray *phoSelTCA =  new TClonesArray("Photon");
    TClonesArray *jetSelTCA =  new TClonesArray("Jet");

	TH1F *h1_TowerEta = new TH1F("h1_TowerEta","h1_TowerEta",100,-6,6);



// --Event number parameters
	int totalEvt = (int)inChain->GetEntries();
	int per99 = totalEvt/99;
	int per100 = 0;
	int step0num =0;
	int step1num =0;
    int step2num =0;
    int step2_Zmass =0;
    int step3num =0;
	double ntgenN =totalEvt;

	cout << " Input Events are: " << totalEvt << endl;

// --Tree for making ntuples
	TTree* outTree = new TTree("tree","tree");
	//TTree* imageTree = new TTree("image","image");

	vector<double> ntTowerEta	;
	vector<double> ntTowerPhi	;
	vector<double> ntTowerE		;
	vector<double> ntTowerEem	;
	vector<double> ntTrackEta	;
	vector<double> ntTrackPhi	;
	double Tower_size		;
	double Track_size		;

	double ntele1PT		;
	double ntele2PT		;
	double ntele1Eta	;
	double ntele2Eta	;
	double ntele1Phi	;
	double ntele2Phi	;
	double nteeM		;
	double ntphoPT		;
	double ntphoEta		;
	double ntphoPhi		;
	double ntjet1PT		;
	double ntjet2PT		;
	double ntjet1Eta	;	 
	double ntjet2Eta	;
	double ntjet1Phi	;
	double ntjet2Phi	;
	double ntjjM		;
	double ntjdEta		;
	double ntjdPhi		;
	double ntZpVar		;
	
	outTree->Branch("ntTowerEta",&ntTowerEta) ;
	outTree->Branch("ntTowerPhi",&ntTowerPhi) ;
	outTree->Branch("ntTowerE",&ntTowerE)	 ;
	outTree->Branch("ntTowerEem",&ntTowerEem) ;
	outTree->Branch("ntTrackEta",&ntTrackEta) ;
	outTree->Branch("ntTrackPhi",&ntTrackPhi) ;

	outTree->Branch("ntele1PT",&ntele1PT)		;
	outTree->Branch("ntele2PT",&ntele2PT)		;
	outTree->Branch("ntele1Eta",&ntele1Eta)		;
	outTree->Branch("ntele2Eta",&ntele2Eta)		;
	outTree->Branch("nteeM",&nteeM)				;
	outTree->Branch("ntele1Phi",&ntele1Phi)		;
	outTree->Branch("ntele2Phi",&ntele2Phi)		;
	outTree->Branch("ntphoPT",&ntphoPT)			;
	outTree->Branch("ntphoEta",&ntphoEta)		;
	outTree->Branch("ntphoPhi",&ntphoPhi)		;
	outTree->Branch("ntjet1PT",&ntjet1PT)		;
	outTree->Branch("ntjet2PT",&ntjet2PT)		;
	outTree->Branch("ntjet1Eta",&ntjet1Eta)		; 
	outTree->Branch("ntjet2Eta",&ntjet2Eta)		;
	outTree->Branch("ntjet1Phi",&ntjet1Phi)		;
	outTree->Branch("ntjet2Phi",&ntjet2Phi)		;
	outTree->Branch("ntjjM",&ntjjM)				;
	outTree->Branch("ntjdEta",&ntjdEta)			;
	outTree->Branch("ntjdPhi",&ntjdPhi)			;
	outTree->Branch("ntZpVar",&ntZpVar)			;
	
	outTree->Branch("nttype",&nttype)			;
	outTree->Branch("ntxsec",&ntxsec)			;
	outTree->Branch("ntgenN",&ntgenN)			;


	// ---EventLoop start
	for(int eventLoop=0; eventLoop < totalEvt; eventLoop++) {
		inChain->GetEntry(eventLoop);
		if((eventLoop%per99) == 0) std::cout << "Running " << per100++ << " %" << std::endl;

		eleSelTCA->Clear("C");
        phoSelTCA->Clear("C");
        jetSelTCA->Clear("C");
		//TowerTCA->Clear("C");			
		//TrackTCA->Clear("C");			

		ntTowerEta.clear();
		ntTowerPhi.clear();
		ntTowerE.clear(); 	 
		ntTowerEem.clear();
		ntTrackEta.clear();
		ntTrackPhi.clear();
	
		step0num++;



/////////////////////--Electron Selection 
		// ---Electron Loop start
		for(int eleLoop=0; eleLoop<eleTCA->GetEntries(); eleLoop++){
            Electron *elePtr = (Electron*)eleTCA->At(eleLoop);

			if (elePtr->PT < 25)            continue;
			if(TMath::Abs(elePtr->Eta)>2.5) continue;

			new ((*eleSelTCA)[(int)eleSelTCA->GetEntries()]) Electron(*elePtr);


		}	 // -- Elctron Loop end
		
		if(eleSelTCA->GetEntries() < 2) continue;
		Electron* elePtr1 = (Electron*)eleSelTCA->At(0);
		Electron* elePtr2 = (Electron*)eleSelTCA->At(1);
		if(elePtr1->Charge * elePtr2->Charge == 1 ) continue;
		 step1num++;  


		
/////////////////////--Photon Selection 
	// ---Photon Loop start	
	for(int phoLoop=0; phoLoop<phoTCA->GetEntries(); phoLoop++){
			Photon *phoPtr = (Photon*)phoTCA->At(phoLoop);

			if(phoPtr->PT <25) continue;
			if(TMath::Abs(phoPtr->Eta)>2.5) continue;
			
			double dPhi1 = (phoPtr->Phi)-(elePtr1->Phi);
			double dPhi2 = (phoPtr->Phi)-(elePtr2->Phi);
			double deltaPhi1 = ( dPhi1 > TMath::Pi() ) ? fabs(TMath::TwoPi() - dPhi1) : fabs(dPhi1);
			double deltaPhi2 = ( dPhi2 > TMath::Pi() ) ? fabs(TMath::TwoPi() - dPhi2) : fabs(dPhi2);
			double dEta1 = fabs(phoPtr->Eta - elePtr1->Eta);
			double dEta2 = fabs(phoPtr->Eta - elePtr2->Eta);
			double dR1 = TMath::Sqrt(deltaPhi1*deltaPhi1 + dEta1*dEta1);
			double dR2 = TMath::Sqrt(deltaPhi2*deltaPhi2 + dEta2*dEta2);
			if(dR1 <0.5 || dR2 < 0.5) continue;

		new ((*phoSelTCA)[(int)phoSelTCA->GetEntries()]) Photon(*phoPtr);


		} // Photon Loop end
		
		if(phoSelTCA->GetEntries() < 1 )  continue;

	    step2num++;

	    Photon* phoPtr = (Photon*)phoSelTCA->At(0);
		
		
/////////////////////--Z mass window
	TLorentzVector ele1Vec = elePtr1->P4();
	TLorentzVector ele2Vec = elePtr2->P4();
	TLorentzVector eeVec = ele1Vec + ele2Vec;
	//if(eeVec.M() < 60 || eeVec.M() > 120) continue;
	
	step2_Zmass++;
	

		// if(jetTCA->GetEntries() != 0 ) {
		// Jet* jetPtr = (Jet*)jetTCA->At(0);
		// h1_jetPT->Fill(jetPtr->PT);
		// }
		// h1_Njet->Fill(jetTCA->GetEntries());
	
/////////////////////--Jet Selection 
	// ---Jet Loop start
	for(int jetLoop=0; jetLoop<jetTCA->GetEntries(); jetLoop++){
        Jet *jetPtr = (Jet*)jetTCA->At(jetLoop);

        if(TMath::Abs(jetPtr->Eta)>4.7) continue;
        if(jetPtr->PT < 30) continue;
			

			double dPhi = (phoPtr->Phi)-(jetPtr->Phi);
			double deltaPhi = ( dPhi > TMath::Pi() ) ? fabs(TMath::TwoPi() - dPhi) : fabs(dPhi);
			double dEta = fabs(phoPtr->Eta - jetPtr->Eta);
			double dR = TMath::Sqrt(deltaPhi*deltaPhi + dEta*dEta);
			if(dR <0.5) continue;


	
	new ((*jetSelTCA)[(int)jetSelTCA->GetEntries()]) Jet(*jetPtr);


    } // Jet Loop End



    
	if(jetSelTCA->GetEntries() < 2) continue;
    step3num++;  

    Jet* jetPtr1 = (Jet*)jetSelTCA->At(0);
    Jet* jetPtr2 = (Jet*)jetSelTCA->At(1);
	


	TLorentzVector phoVec = phoPtr->P4();
	TLorentzVector eeaVec = ele1Vec + ele2Vec+phoVec;
	TLorentzVector jet1Vec = jetPtr1->P4();
    TLorentzVector jet2Vec = jetPtr2->P4();
    TLorentzVector jjVec = jet1Vec + jet2Vec;
	
	// Di-jet mass
	double jjM =jjVec.M();
	
	// Delta Phi "dleta pht needs correction" 
	double dEta = fabs((jetPtr2->Eta) - (jetPtr1->Eta));
    double dPhi = fabs((jetPtr2->Phi) - (jetPtr1->Phi));
    double deltaPhi = ( dPhi > TMath::Pi() ) ? fabs(TMath::TwoPi() - dPhi) : fabs(dPhi); // Correction
    
	
	double rapZA = eeaVec.Rapidity();
    double rapJ1 = jet1Vec.Rapidity();
    double rapJ2 = jet2Vec.Rapidity();
    
	// Zeppenfeld variable
	double zepp = fabs(rapZA - (rapJ1 + rapJ2) / 2.0);



	Tower_size += TowerTCA->GetEntries();
	Track_size += TrackTCA->GetEntries();

	// --Tower Loop for Images 
	for(int TowerLoop=0; TowerLoop<TowerTCA->GetEntries(); TowerLoop++){
		Tower *TowerPtr = (Tower*)TowerTCA->At(TowerLoop);

		ntTowerEta.push_back(TowerPtr->Eta)    ;
        ntTowerPhi.push_back(TowerPtr->Phi)    ;
        ntTowerE.push_back(TowerPtr->E)        ;
        ntTowerEem.push_back(TowerPtr->Eem)    ;

	}
	
	// --Track Loop for Images 
	for(int TrackLoop=0; TrackLoop<TrackTCA->GetEntries(); TrackLoop++){
		Track *TrackPtr = (Track*)TrackTCA->At(TrackLoop);
		
		ntTrackEta.push_back(TrackPtr->Eta)    ;
        ntTrackPhi.push_back(TrackPtr->Phi)    ;
	}
	

		ntele1PT  =	elePtr1->PT		;
		ntele2PT  =	elePtr2->PT		;
		ntele1Eta =	elePtr1->Eta	;
		ntele2Eta =	elePtr2->Eta	;
		ntele1Phi =	elePtr1->Phi	;
		ntele2Phi =	elePtr2->Phi	;
		nteeM	  =	eeVec.M()		;
		ntphoPT	  = phoPtr->PT		;
		ntphoEta  = phoPtr->Eta		;
		ntphoPhi  = phoPtr->Phi		;
		ntjet1PT  = jetPtr1->PT		;
		ntjet2PT  = jetPtr2->PT		;
		ntjet1Eta = jetPtr1->Eta	;
		ntjet2Eta = jetPtr2->Eta	;
		ntjet1Phi = jetPtr1->Phi	;
		ntjet2Phi = jetPtr2->Phi	;
		ntjjM	  = jjM				;
		ntjdEta	  = dEta			;
		ntjdPhi   = deltaPhi		;
		ntZpVar   = zepp			;
	
		outTree->Fill();
	} //--Event Loop end


	cout << "track size: " << Track_size << endl;
	cout << "tower size: " << Tower_size << endl;
	cout << "step0 :" << step0num << endl;
	cout << "step1 :" << step1num << endl;
    cout << "step2 :" << step2num << endl;
    cout << "Zmasswindow :" << step2_Zmass << endl;
    cout << "step3 :" << step3num << endl;
	cout << (double)step3num / step0num * 100 << "%" << endl;

	outFile->Write();
	return 0;

}
