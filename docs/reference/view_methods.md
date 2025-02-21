# View Methods Index

Below you'll find all of the methods of View, including associated operations and ways of creating them.
## View Operations


### `product`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L811)

```

        Based on definition 5.15, p208

        Γ^θ_fRI ⨂ᵀ Δ^{Ψ}_gSJ = (Γ_f ⨂ Δ^{Ψ}_g)^θ_(T⋈R)⋈(T⋈S),I∪J

        where Γ_f ⨂ Δ^{Ψ}_g = P + Σ_γ∈(Γ＼P) Σ_δ∈Δ {f(γ) x g(δ)).(γ∪δ)}
        and P = {f(γ).γ∈Γ |¬∃ψ ∈ Ψ.ψ⊆γ}

        Args:
            self (View): Γ^θ_fRI
            view (View): Δ^{Ψ}_gSJ
            inherited_dependencies (Optional[DependencyRelation], optional): T. Defaults to an empty
                dependency relation.

        Returns:
            View: The result of the product calculation.
        
```

### `sum`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L851)

```

        Based on definition 5.14, p208

        Γ^θ_fRI ⊕ᵀ Δ^{0}_gSJ = (Γ_f + Δ_g)^θ_(T⋈R)⋈(T⋈S),I∪J

        where (Γ_f + Δ_g) = (Γ ∪ Δ)_h, where h(γ) = f(γ) + g(γ)

        Args:
            self (View): Γ^θ_fRI
            view (View): Δ^{0}_gSJ
            inherited_dependencies (Optional[DependencyRelation], optional): T. Defaults to an empty
                dependency relation.

        Returns:
            View: The result of the sum calculation
        
```

### `update`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L1165)

```

        Based on Definition 4.34, p163

        Γ^Θ_fRI[D]^↻ = Γ^Θ_fRI[D]ᵁ[D]ᴱ[D]ᴬ[D]ᴹ

        Args:
            self (View): Γ^Θ_fRI
            view (View): D
            verbose (bool, optional): Enables verbose mode. Defaults to False.

        Returns:
            View: The updated view.
        
```

### `answer`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L1016)

```

        Based on definition 5.13, p206

        Γ^θ_fRI[Δ^{0}_gSJ]^A = Γ^θ_fRI[Δ^{0}_gSJ]^𝔼A[Δ^{0}_gSJ]^𝓐A

        Args:
            self (View): Γ^θ_fRI
            other (View): Δ^{0}_gSJ
            verbose (bool, optional): enables verbose mode

        Returns:
            View: The result of the answer calculation
        
```

### `negation`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L1039)

```

        Based on definition 5.16, p210

        [Γ^Θ_fRI]ᶰ = (Θ ⨂ [Γ]ᶰ)^{0}_[R]ᶰ[I]ᶰ

        Args:
            self (View): Γ^Θ_fRI
            verbose (bool, optional): enable verbose mode. Defaults to False.

        Returns:
            View: The negated view.
        
```

### `merge`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L1067)

```

        Based on Definition 5.26, p221

        Γ^Θ_fRI[Δ^Ψ_gSJ]ᴹ = ⊕^R⋈S_γ∈Γ {f(γ).γ}|^Θ_RI ⨂^R⋈S Δ^Ψ_gSJ ⨂^R⋈S (⭙^R⋈S_<t,u>∈M'ij(γ) Sub^R⋈S_<t,u>(Δ^{0}_gSJ))

        Args:
            self (View): Γ^Θ_fRI
            view (View): Δ^Ψ_gSJ
            verbose (bool, optional): enable verbose mode. Defaults to False.

        Returns:
            View: Returns the merged view.
        
```

### `division`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L1452)

```

        Based on definition 4.38, p168

        If ∀δ_∈Δ ∃ψ_∈Ψ ∃γ∈Γ (δ ⊆ γ ∧ ψ ⊆ γ):

        Γ^Θ_RI ⊘ Δ^Ψ_SJ = {γ ⊘_Γ Δ^Ψ : γ∈Γ}^Θ_[R][I]

        Args:
            self (View): Γ^Θ_fRI
            view (View): Δ^Ψ_SJ
            verbose (bool, optional): Enables verbose mode. Defaults to False.

        Returns:
            View: The divided view.
        
```

### `factor`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L1500)

```

        Based on definition 5.17 p210 (contradiction)
        Based on definition 5.35 p233 (identity)
        Based on definition 5.32 p232 (central case)

        Contradiction: Γ^Θ_fRI[⊥]ꟳ = {γ∈Γ : ¬∃κ ∈ 𝕂.κ ⊆ γ}^Θ_fRI
        Identity: Γ^Θ_fRI[{w.t₁==t₂}^{0}_gSJ]ꟳ = {γ ∈ Γ : t₁==t₂ ∉ γ}_f + Σ_γ∈Γ s.t.t₁==t₂∈γ {(f(γ)[t₁/t₂]).(γ[t₁/t₂])}^Θ_RI
        Central: Γ^Θ_fRI[Δ^Ψ_gSJ]ꟳ = Σ_γ∈Γ {f(γ).γ[Δ^Ψ]ꟳ}

        Args:
            self (View): Γ^Θ_fRI
            other (View): ⊥ | {w.t₁==t₂}^{0}_gSJ | Δ^Ψ_gSJ
            verbose (bool, optional): Enables verbose mode. Defaults to False.
            absurd_states (Optional[list[State]], optional): Manual input of primitive absurd states. Defaults to None.

        Returns:
            View: The factored view.
        
```

### `depose`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L1684)

```

        Based on definition 5.23

        Γ^Θ_fRI[]ᴰ = (Γ_f + [Θ]ᶰ)^{0}_R[I]ᶰ

        Args:
            verbose (bool, optional): Enables verbose mode. Defaults to False.

        Returns:
            View: The deposed view.
        
```

### `inquire`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L1715)

```

        Based on definition 5.18, p210


        If A(Γ∪Θ) ∩ A(Δ∪Ψ) = ∅ and A(Δ) ∩ A(Ψ) = ∅
            O Case: Γ^Θ_fRI[Δ^Ψ_gSJ]ᴵ = (Γ^Θ_fRI ⨂ (Δ^Ψ_gSJ ⊕ˢ({0}^Ψ_SJ ⨂ ([Δ^{0}_gSJ]ᶰ)^nov(A(Δ)))))[⊥]ꟳ

        Else if A(Δ∪Ψ) ⊆ A(Γ∪Θ) and S = [R]_Γ∪Θ
            I Case: Γ^Θ_fRI[Δ^Ψ_gSJ]ᴵ = (Γ^Θ_fRI ⨂ᴿ (Δ^Ψ_gSJ ⊕ᴿ ([Δ_g]ᶰ|^Ψ_SJ)))[⊥]ꟳ

        Else:
            Γ^Θ_fRI[Δ^Ψ_gSJ]ᴵ = Γ^Θ_fRI
        Args:
            self (View): Γ^Θ_fRI
            other (View): Δ^Ψ_gSJ
            verbose (bool, optional): Enables verbose mode. Defaults to False.

        Returns:
            View: The resultant inquired view.
        
```

### `suppose`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L1808)

```

        Based on definition 5.22, p219

        If A(Γ∪Θ) ∩ A(Δ∪Ψ) = ∅ ∧ Δ^Ψ_gSJ = Δ^Ψ_SJ
            O Case: Γ^Θ_fRI[Δ^Ψ_gSJ]ˢ = Γ^Θ'_[R⋈R'][I∪I'] [Δ^Ψ_gSJ]ᵁ[Δ^Ψ_gSJ]ᴱ[Δ^Ψ_gSJ]ᴬ[Δ^Ψ_gSJ]ᴹ

            where: Θ'^{0}_R'I' = Θ^{0}_RI ⨂ Nov(Δ^Ψ_[S]ᶰJ []ᴰ)

        Else if A(Δ) ⊆ A(Γ∪Θ), [R]_Δ = S, and Δ^Ψ_gSJ = Δ^Ψ_SJ and Ψ = {0}
            I Case: Γ^Θ_fRI[Δ^{0}_gSJ]ˢ = Γ^(Θ⨂Δ)_fRI[Δ^{0}_gSJ]ᵁ[Δ^{0}_gSJ]ᴱ[Δ^{0}_gSJ]ᴬ[Δ^{0}_gSJ]ᴹ

        Else:
            Γ^Θ_fRI[Δ^Ψ_gSJ]ˢ = Γ^Θ_fRI

        Args:
            self: (View): Γ^Θ_fRI
            other (View): Δ^Ψ_gSJ
            verbose (bool, optional): Enables verbose mode. Defaults to False.

        Returns:
            View: The resultant view.
        
```

### `query`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L1927)

```

        Based on definition 5.19, p210
        If U_S ⊆ U_R:
            Γ^Θ_fRI[Δ^Ψ_gSJ]ꟴ = H + Σ_γ∈Γ Σ_δ∈Δ_s.t.Φ(γ, δ) {w_(γ,δ).δ}^Θ_R⋈<U_R,E_S＼E_R,D_S'>,I∪J
        Else:
            Γ^Θ_fRI[Δ^Ψ_gSJ]ꟴ = Γ^Θ_fRI
        
```

### `which`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L2102)

```

        Based on definition 5.33, p232

        Γ^Θ_fRI[Δ^Ψ_gSJ]ᵂ = H + Σ_γ∈Γ《ω.ξ : Ξ(γ,ω.ξ)》|^Θ_RI

        Ξ(γ,ω.ξ) = ∃ψ_∈Ψ ∃δ_∈Δ ∃n≥0 ∃<t₁,e₁>,...,<tₙ,eₙ>∈M'ij (∀i,j.(e_i=e_j -> i=j)) ∧ (ξ∪ψ ⊆ γ ∧ ω.ξ = (g(δ).δ)[t₁/e₁,...,tₙ/eₙ])

        Args:
            self (View): Γ^Θ_fRI
            other (View): Δ^Ψ_gSJ
            verbose (bool, optional): Enables verbose mode. Defaults to False.

        Returns:
            View: The resultant view.
        
```

### `universal_product`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L1212)

```

        Based on Definition 5.28, p223

        Γ^Θ_fRI[D]ᵁ = {0}^Θ_RI ⨂^R⋈S (⨂^R⋈S_<u,t>∈M'ij Sub^R⋈S_<t,u> (Γ^{0}_fRI))
        
```

### `atomic_answer`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L899)

```

        Based on definition 5.12, p206

        Γ^θ_fRI[Δ^{0}_gSJ]^𝓐A = argmax_γ∈Γ(Δ[{{p} : p ∈ γ}]^𝓐P)_f |^θ_RI

        Args:
            self (View): Γ^θ_fRI
            other (View): Δ^{0}_gSJ
            verbose (bool, optional): enables verbose mode

        Returns:
            View: The result of the atomic answer calculation
        
```

### `equilibrium_answer`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L954)

```

        Based on definition 5.10, p205

        Γ^θ_fRI[Δ^{0}_gSJ]^𝔼A

        Args:
            self (View): Γ^θ_fRI
            other (View): Δ^{0}_gSJ
            verbose (bool, optional): enables verbose mode

        Returns:
            View: The result of the equilibrium answer calculation
        
```

### `existential_sum`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L1286)

```

        Based on Definition 5.34, p233

        Γ^Θ_fRI[Δ^{0}_gSJ]ᴱ = Γ^Θ_fRI ⊕^R⋈S (
            ⊕^R⋈S_<e,t>∈M'ij Sub^R⋈S_<t,e> (BIG_UNION(e)^Θ_SJ)
        )
        
```

## Parsing


### `from_str`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L2214)

```

        Parses from view string form to view form.

        Args:
            s (str): view string
            custom_functions (list[NumFunc | Function] | None, optional): Custom functions used in the
                string. It assumes the name of the function is that used in the string. Useful
                for using func callers. Defaults to None.

        Returns:
            View: The output view
        
```

### `to_str`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L2232)

```

        Parses from View form to view string form

        Args:
            v (View): The view to convert to string

        Returns:
            str: The view string
        
```

### `from_fol`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L2244)

```

        Parses from first order logic string form to View form.
        Args:
            s (str): A first order logic string
            custom_functions (list[NumFunc | Function] | None, optional): Custom functions used in the
                string. It assumes the name of the function is that used in the string. Useful
                for using func callers. Defaults to None.
        Returns:
            View: The parsed view
        
```

### `to_fol`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L2260)

```

        Parses from View form to first order logic string form.

        Args:
            v (View): The View object

        Returns:
            str: The first order logic string form.
        
```

### `from_json`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L2189)

```

        Parses from json form to View form

        Args:
            s (str): The json string

        Returns:
            View: The parsed view
        
```

### `to_json`

[Link to code](https://github.com/dreamingspires/PyETR/blob/master/pyetr/view.py#L2202)

```

        Parses from View form to json form

        Args:
            v (View): The input view

        Returns:
            str: The output json
        
```