from swarmalator_model import run_swarmalator as run, swarmalator
import tkinter

def main():
    screen_size = 1000
    no_of_swarmalators = 50
    delta_t = 0.1
    coupling_probability = 0.1
    J = 1.0
    K = 0

    window = tkinter.Tk()
    canvas = run.initialise_canvas(window, screen_size)

    list_of_swarmalators = run.create_swarmalators(canvas, no_of_swarmalators, screen_size)

    run.step(canvas, list_of_swarmalators, screen_size, delta_t=delta_t, J = J, K = K, coupling_probability=coupling_probability, animation_speed=1)

    window.mainloop()


if __name__ == "__main__":
    main()