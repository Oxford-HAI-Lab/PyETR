# Inference Index

Below you'll find all of the cases in pyetr.cases, and their associated views. You can use this page as an index of the current cases.

## `basic_step`
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/inference.py#L34)


```

    Based Definition 4.47 p179-180

    G' = T[P₁[]ᴰ]^↻[P₂]^↻...[Pₙ]^↻[⊥]ꟳ

    Args:
        v (Sequence[View]): (P₁,..., Pₙ)
        verbose (bool, optional): Enables verbose mode. Defaults to False.

    Returns:
        View: G'
    
```

## `default_inference_procedure`
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/inference.py#L56)


```

    Based Definition 4.47 p179-180

    G' = T[P₁[]ᴰ]^↻[P₂]^↻...[Pₙ]^↻[⊥]ꟳ
    G'' = G'[P₁[]ᴰ]ꟳ...[Pₙ]ꟳ

    Args:
        v (Sequence[View]): (P₁,..., Pₙ)
        verbose (bool, optional): Enables verbose mode. Defaults to False.

    Returns:
        View: G''
    
```

## `default_procedure_does_it_follow`
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/inference.py#L95)


```

    Based Definition 4.47 p180

    (Sub-procedure for "does Δ^Ψ_RI follow?" tasks)
    G' = T[P₁[]ᴰ]^↻[P₂]^↻...[Pₙ]^↻[⊥]ꟳ
    G'' = G'[Ψ^{0}_[R][I]]ˢ[Δ^Ψ_RI]ꟴ

    Args:
        v (Sequence[View]): (P₁,..., Pₙ)
        target View: Δ^Ψ_RI
        verbose (bool, optional): Enables verbose mode. Defaults to False.

    Returns:
        bool: Report yes or no, note: Report G'' -> yes
    
```

## `default_procedure_what_is_prob`
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/inference.py#L139)


```

    Based on definition 5.20, p212

    G' = T[P₁]^↻[]ᴰ[P₂]^↻...[Pₙ]^↻[⊥]ꟳ
    G'' = G'[Δ^Ψ]ꟴ

    If G''[Δ]^𝔼P ∈ [0,100]:
        return G''
    Else
        x = (100 - (Σ_γ∈ΓΣ《α ∈ f(γ) : α ∈ ℝ》)) / #{γ∈Γ : f(γ) =《》}

        where γ₁...γₙ is {γ ∈ Γ : f(γ) =《》}
        G'' = G'[{《x》.0 }^{γ₁}]ᴵ...[{《x》.0 }^{γₙ}]ᴵ[Δ^Ψ]ꟴ

        If G''[Δ]^𝔼P ∈ [0,100]:
            return G''
        Else:
            return ⊥
    Args:
        v (Sequence[View]): (P₁,..., Pₙ)
        prob_of (View): Δ^Ψ
        verbose (bool, optional): Enables verbose mode. Defaults to False.

    Returns:
        View: G''
    
```

## `default_decision`
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/inference.py#L233)


```

    Based on Definition 6.7, p272

    dq[dq[CV]^↻[⊥]ꟳ[PR]^↻]

    Args:
        dq (View): dq, Decision Question
        cv (Iterable[View]): CV, Consequence Views
        pr (Iterable[View]): PR, Priority Views
        verbose (bool, optional): Enable verbose mode. Defaults to False.
        absurd_states (Optional[list[State]], optional): Any additional absurd states in the system. Defaults to None.

    Returns:
        View: The resultant view.
    
```

## `classically_valid_basic_step`
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/inference.py#L269)


```

    Same as basic_step, except we inquire on all atoms in the original view to preserve alternatives
    in a classically valid way.
    
```

## `classically_valid_inference_procedure`
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/inference.py#L287)


```

    Same as default_inference_procedure, except we inquire on all atoms in the original view to preserve
    alternatives in a classically valid way.
    
```

## `classically_valid_does_it_follow`
[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/inference.py#L319)


```

    Same as default_procedure_does_it_follow, except we inquire on all atoms in the original view to preserve
    alternatives in a classically valid way.
    
```