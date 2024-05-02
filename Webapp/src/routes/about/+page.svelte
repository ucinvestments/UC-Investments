<div class="m-1">
	<h2>Methodology</h2>
<p>Currently, we have roughly analyzed $108 billion of the UC's total investment portfolio. We've specifically analyzed 
	the composition of funds that total up to about $49B. A majority of these funds are 
	stored in the UC Retirement Plan (UCRP) ($89.2B) and in the General Endowment Pool (GEP) 
	($20.7B) Nearly all of the UC's money that goes to companies happens indirectly, 
	through the use of investing in index funds, public equity funds, and private hedge funds.</p>

<p>Some of these funds publish full composition data, but most do not. For example, our 
	largest investment, in a fund managed by MSCI, only publishes its top 10 holdings, 
	which only explains where 18% of this money goes. We employed 
	three main strategies to provide accurate estimates:</p>

<ul>
  <li>
    • Using provided data:
    <ul>
      <li>In the instance that a fund released its composition, we simply use this data.</li>
    </ul>
  </li>
  <li>
    • Reconstructing data through re-weighting:
    <ul>
      <li>
        Some of our largest investments, such as our $35B investment in the MSCI ACWI IMI TF EX-TOB AND FF fund, only release its top 10 holdings. They do, however, release the full composition of the non-ex-tobacco/ex-fossil fuel version of this fund (MSCI ACWI IMI).
      </li>
      <li>
        With this composition data, we conduct a re-weighting procedure. We go through every company that this fund is invested in, checking it against a list of fossil fuel and tobacco companies, and removing those assets.
      </li>
      <li>
        After pruning, we distribute the remaining weight across all companies proportional to their original weights, giving us a rough estimate of the composition of the specific fund the UC is invested in.
      </li>
      <li>
        This isn't a perfect system, but it's our best method for estimating what these specific funds are comprised of.
      </li>
    </ul>
  </li>
  <li>
    • Using SEC filings:
    <ul>
      <li>
        In the case of direct investments we have in hedge funds, we use a combination of SEC forms 13F, 13D, and G to discover their holdings. This data is obtained from sites such as whalewisdom.com.
      </li>
    </ul>
  </li>
</ul>

<p>For some assets, though, we gain little to no data. This is especially true with investments in foreign hedge funds that aren't required to file anything with the SEC or publish any of their holdings.</p>

<p>Once we've determined the holdings of the funds the UC is invested in, we multiply the weight of each company in each individual fund by the total amount invested in that asset, determining how much money is indirectly going to such a company.</p>

<p>Across all of the individual fund composition datasets, companies are often spelled slightly differently, due to abbreviations. We standardize these abbreviations and use a fuzzing match process to group investments. Funds also invest in different classes of each stock, and when listed, we differentiate these holdings unless you click "combine stock classes."</p>

	
	<h2>Sources</h2>
<p> Our research began by looking at both the UCRP and GEP holding documents published on the UC's investment page. The data for the funds we analyzed came from a variety of sources as stated above, and all specific sources can be <a
href="https://github.com/g4cko/UC-Investments/tree/main/Data-Collection/csv-files">found here.</a> </p>
	<h2>Contribute</h2>
	<p> If you'd like to help continue this research by either contributing to data research or programming, check out this project's (incredibly disorganized) <a
	href="https://github.com/g4cko/UC-Investments/">Github repository.</a> </p>
	<h2>About</h2>
	<p> This project was started due to the conversations accross college campuses about divesting from Israel. The first demand with most of these protests is disclosure of investment holdings, as most of the colleges where these protests were taking place were private, and did not have to publish this data. Luckily, as students within the UC system, we are given some data on our investment holdings, which allowed us to analyze them.

	The research and backend programming was done by <a href="https://www.linkedin.com/in/alex-k-forman/" Alex Forman ></a> and the frontend of this site was built by <a href="https://stephenokita.com/"> Stephen Okita</a> </p>
	<br>
	<br>
	<p> If you'd like to reach out with any questions, suggestions or concerns, please email aforman + @ + berkeley.edu </p>
	<br/></div>

<style>
	div {
		padding-left: 2rem;
		padding-right: 2rem;
	}
	h1 {
		color: var(--pri);
		font-size: 5vw;
	}
	h2 {
		color: var(--pri);
		font-size: 3vw;
	}
	p {

	}
	h3 {
		margin-top: 1rem;
		font-size: 2vw;
		color: var(--sec);
		text-decoration-line: underline;
	}
	li {
		margin-left: 1rem;
	}
	a {
		color: var(--sec);
		text-decoration-line: underline;
	}
	@media (max-width: 580px) {
		h1 {
			font-size: 10vw;
		}
		h2 {
			font-size: 5vw;
		}
		p {
			font-size: 4vw;
		}
		h3 {
			font-size: 5vw;
		}
		h4 {
			font-size: 4.5vw;
		}
	}
</style>