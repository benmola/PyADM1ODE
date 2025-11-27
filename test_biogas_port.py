import sys
import os
import numpy as np

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from biogas import substrates, substrate, ADMstate, digester, chemistry
    print("Successfully imported biogas package.")
except ImportError as e:
    print(f"Failed to import biogas package: {e}")
    sys.exit(1)

def test_substrates_loading():
    print("Testing substrates loading...")
    try:
        subs = substrates('substrate_gummersbach.xml')
        print(f"Loaded {subs.getNumSubstrates()} substrates.")
        
        # Check a parameter
        sub1 = subs.get(1)
        print(f"Substrate 1: {sub1.name}")
        ts = sub1.get_param_of_d("TS")
        print(f"TS of Substrate 1: {ts}")
        
        if ts == 0:
            print("Warning: TS is 0, might be parsing error.")
            
    except Exception as e:
        print(f"Error loading substrates: {e}")
        raise

def test_simulation_step():
    print("Testing simulation step...")
    try:
        from feedstock import Feedstock
        from PyADM1 import PyADM1, get_state_zero_from_initial_state
        
        # Initialize
        fs = Feedstock(48)
        adm1 = PyADM1(fs)
        
        # Create influent
        Q = [15, 10, 10, 0, 0, 0, 0, 0, 0, 0]
        adm1.createInfluent(Q, 0)
        print("Influent created.")
        
        # Initial state
        state_zero = get_state_zero_from_initial_state("digester_initial8.csv")
        print("Initial state loaded.")
        
        # Run ODE step
        # Just call ADM1_ODE directly to check for errors
        t = 0
        dstate = adm1.ADM1_ODE(t, state_zero)
        print("ADM1_ODE executed successfully.")
        print(f"Derivative vector shape: {len(dstate)}")
        
    except Exception as e:
        print(f"Error during simulation step: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    test_substrates_loading()
    test_simulation_step()
    print("Verification complete.")
